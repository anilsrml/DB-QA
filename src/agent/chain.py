"""LangChain zincirleri ve LLM entegrasyonu (Ollama/Gemini)"""

import json
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .prompts import (
    SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES,
    QUERY_GENERATION_PROMPT,
    RESULT_EXPLANATION_PROMPT,
    ERROR_EXPLANATION_PROMPT,
    CLARIFICATION_PROMPT,
)
from ..config import settings
from ..utils.logger import logger


class LLMChainManager:
    """LangChain ve LLM yöneticisi (Ollama/Gemini)"""
    
    def __init__(self, temperature: float = 0.1):
        """
        LLM chain manager'ı başlat
        
        Args:
            temperature: Model yaratıcılık seviyesi (0-1)
        """
        self.temperature = temperature
        self.provider = settings.llm_provider.lower()
        self.llm = self._initialize_llm()
        logger.info("LLMChainManager initialized", 
                   provider=self.provider, 
                   temperature=temperature)
    
    def _initialize_llm(self):
        """
        LLM'i başlat (Ollama veya Gemini)
        
        Returns:
            LLM instance
        """
        try:
            if self.provider == "ollama":
                return self._initialize_ollama()
            elif self.provider == "gemini":
                return self._initialize_gemini()
            else:
                raise ValueError(f"Desteklenmeyen LLM provider: {self.provider}")
        except Exception as e:
            logger.error("Failed to initialize LLM", provider=self.provider, error=str(e))
            raise
    
    def _initialize_ollama(self) -> Ollama:
        """
        Ollama LLM'i başlat (Lokal model)
        
        Returns:
            Ollama instance
        """
        llm = Ollama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=self.temperature,
        )
        logger.info("Ollama LLM initialized successfully", 
                   model=settings.ollama_model,
                   base_url=settings.ollama_base_url)
        return llm
    
    def _initialize_gemini(self) -> ChatGoogleGenerativeAI:
        """
        Gemini LLM'i başlat (Google Cloud)
        
        Returns:
            ChatGoogleGenerativeAI instance
        """
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY gerekli ama .env dosyasında bulunamadı")
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.google_api_key,
            temperature=self.temperature,
            convert_system_message_to_human=True,
        )
        logger.info("Gemini LLM initialized successfully")
        return llm
    
    def generate_sql(
        self,
        question: str,
        schema: str,
        include_examples: bool = True,
    ) -> Dict[str, Any]:
        """
        Doğal dil sorusundan SQL oluştur
        
        Args:
            question: Kullanıcının sorusu
            schema: Veritabanı schema bilgisi
            include_examples: Few-shot örnekleri dahil et
        
        Returns:
            SQL ve metadata içeren dict
        """
        try:
            # Prompt oluştur
            few_shot = FEW_SHOT_EXAMPLES if include_examples else ""
            
            prompt_template = PromptTemplate(
                input_variables=["schema", "few_shot_examples", "question"],
                template=SYSTEM_PROMPT + "\n\n" + QUERY_GENERATION_PROMPT,
            )
            
            # Chain oluştur (LangChain 0.3 yeni API)
            chain = prompt_template | self.llm | StrOutputParser()
            
            # SQL oluştur
            logger.info("Generating SQL", question=question[:100])
            response = chain.invoke({
                "schema": schema,
                "few_shot_examples": few_shot,
                "question": question,
            })
            
            # JSON parse et
            result = self._parse_json_response(response)
            
            logger.info(
                "SQL generated successfully",
                sql=result.get("sql", "")[:100],
                confidence=result.get("confidence"),
            )
            
            return result
            
        except Exception as e:
            logger.error("Failed to generate SQL", error=str(e))
            return {
                "sql": None,
                "explanation": f"SQL oluşturma hatası: {str(e)}",
                "confidence": 0.0,
                "tables_used": [],
                "error": str(e),
            }
    
    def explain_results(
        self,
        question: str,
        sql: str,
        results: list,
    ) -> str:
        """
        Sorgu sonuçlarını doğal dilde açıkla
        
        Args:
            question: Kullanıcının sorusu
            sql: Çalıştırılan SQL
            results: Sorgu sonuçları
        
        Returns:
            Türkçe açıklama
        """
        try:
            # Sonuçları formatla (çok uzunsa kısalt)
            results_text = self._format_results_for_llm(results)
            
            prompt_template = PromptTemplate(
                input_variables=["question", "sql", "results"],
                template=RESULT_EXPLANATION_PROMPT,
            )
            
            chain = prompt_template | self.llm | StrOutputParser()
            
            explanation = chain.invoke({
                "question": question,
                "sql": sql,
                "results": results_text,
            })
            
            logger.info("Results explained successfully")
            return explanation.strip()
            
        except Exception as e:
            logger.error("Failed to explain results", error=str(e))
            return f"Sonuç açıklama hatası: {str(e)}"
    
    def explain_error(
        self,
        question: str,
        sql: str,
        error: str,
    ) -> str:
        """
        Hata mesajını kullanıcı dostu şekilde açıkla
        
        Args:
            question: Kullanıcının sorusu
            sql: Hatalı SQL
            error: Hata mesajı
        
        Returns:
            Türkçe hata açıklaması
        """
        try:
            prompt_template = PromptTemplate(
                input_variables=["question", "sql", "error"],
                template=ERROR_EXPLANATION_PROMPT,
            )
            
            chain = prompt_template | self.llm | StrOutputParser()
            
            explanation = chain.invoke({
                "question": question,
                "sql": sql,
                "error": error,
            })
            
            return explanation.strip()
            
        except Exception as e:
            logger.error("Failed to explain error", error=str(e))
            return f"Bir hata oluştu: {error}"
    
    def request_clarification(
        self,
        question: str,
        schema: str,
    ) -> str:
        """
        Belirsiz sorular için açıklama iste
        
        Args:
            question: Kullanıcının sorusu
            schema: Veritabanı schema'sı
        
        Returns:
            Açıklama isteği mesajı
        """
        try:
            prompt_template = PromptTemplate(
                input_variables=["question", "schema"],
                template=CLARIFICATION_PROMPT,
            )
            
            chain = prompt_template | self.llm | StrOutputParser()
            
            clarification = chain.invoke({
                "question": question,
                "schema": schema,
            })
            
            return clarification.strip()
            
        except Exception as e:
            logger.error("Failed to request clarification", error=str(e))
            return "Sorunuzu daha açık bir şekilde sorabilir misiniz?"
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        LLM yanıtından JSON parse et
        
        Args:
            response: LLM yanıtı
        
        Returns:
            Parse edilmiş dict
        """
        try:
            # JSON bloğunu bul
            response = response.strip()
            
            # Markdown code block'ları temizle
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1])
            
            # JSON parse et
            parsed = json.loads(response)
            
            # Gerekli alanları kontrol et
            if "sql" not in parsed:
                raise ValueError("Response does not contain 'sql' field")
            
            # Varsayılan değerler
            parsed.setdefault("explanation", "")
            parsed.setdefault("confidence", 0.5)
            parsed.setdefault("tables_used", [])
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse JSON response", error=str(e))
            # Fallback: SQL'i regex ile bul
            return self._fallback_sql_extraction(response)
    
    def _fallback_sql_extraction(self, response: str) -> Dict[str, Any]:
        """
        JSON parse başarısız olursa SQL'i çıkarmaya çalış
        
        Args:
            response: LLM yanıtı
        
        Returns:
            SQL içeren dict
        """
        import re
        
        # SELECT ile başlayan satırı bul
        match = re.search(r'SELECT.*?;', response, re.IGNORECASE | re.DOTALL)
        
        if match:
            sql = match.group(0)
            return {
                "sql": sql,
                "explanation": "SQL otomatik olarak çıkarıldı",
                "confidence": 0.3,
                "tables_used": [],
            }
        
        return {
            "sql": None,
            "explanation": "SQL oluşturulamadı",
            "confidence": 0.0,
            "tables_used": [],
            "error": "Could not parse response",
        }
    
    def _format_results_for_llm(self, results: list, max_rows: int = 10) -> str:
        """
        Sonuçları LLM için formatla
        
        Args:
            results: Sorgu sonuçları
            max_rows: Maksimum gösterilecek satır sayısı
        
        Returns:
            Formatlanmış sonuç metni
        """
        if not results:
            return "Sonuç bulunamadı."
        
        # İlk N satırı al
        limited_results = results[:max_rows]
        
        # JSON formatında string'e çevir
        results_text = json.dumps(limited_results, ensure_ascii=False, indent=2)
        
        if len(results) > max_rows:
            results_text += f"\n\n... ve {len(results) - max_rows} satır daha."
        
        return results_text

