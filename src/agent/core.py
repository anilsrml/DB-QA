"""Ana AI Agent sınıfı"""

from typing import Dict, Any, Optional, List
from ..database.connection import DatabaseConnection
from ..database.schema_manager import SchemaManager
from ..database.executor import QueryExecutor
from ..validation.sql_validator import SQLValidator, ValidationError
from .chain import LLMChainManager
from ..utils.logger import logger


class QueryAgent:
    """Doğal dil sorgularını SQL'e çeviren ve çalıştıran AI agent"""
    
    def __init__(
        self,
        db_connection: DatabaseConnection,
        temperature: float = 0.1,
    ):
        """
        Query agent'ı başlat
        
        Args:
            db_connection: Veritabanı bağlantısı
            temperature: LLM yaratıcılık seviyesi
        """
        self.db = db_connection
        self.schema_manager = SchemaManager(db_connection)
        self.validator = SQLValidator(strict_mode=True)
        self.executor = QueryExecutor(db_connection, self.validator)
        self.llm_chain = LLMChainManager(temperature=temperature)
        
        # Schema'yı önbellekte tut
        self._cached_schema: Optional[str] = None
        
        logger.info("QueryAgent initialized")
    
    def query(
        self,
        question: str,
        explain_results: bool = True,
        return_raw: bool = False,
    ) -> Dict[str, Any]:
        """
        Doğal dil sorusunu işle ve cevapla
        
        Args:
            question: Kullanıcının Türkçe sorusu
            explain_results: Sonuçları LLM ile açıkla
            return_raw: Ham sonuçları da döndür
        
        Returns:
            Sorgu sonuçları ve metadata
        """
        logger.info("Processing query", question=question)
        
        result = {
            "question": question,
            "sql": None,
            "results": None,
            "explanation": None,
            "success": False,
            "error": None,
            "metadata": {},
        }
        
        try:
            # 1. Schema bilgisini al
            schema = self._get_schema()
            
            # 2. SQL oluştur
            sql_result = self.llm_chain.generate_sql(
                question=question,
                schema=schema,
                include_examples=True,
            )
            
            if not sql_result.get("sql"):
                result["error"] = sql_result.get("explanation", "SQL oluşturulamadı")
                return result
            
            result["sql"] = sql_result["sql"]
            result["metadata"]["confidence"] = sql_result.get("confidence", 0.0)
            result["metadata"]["tables_used"] = sql_result.get("tables_used", [])
            
            # 3. SQL'i valide et
            is_valid, error_msg = self.validator.validate(sql_result["sql"])
            if not is_valid:
                result["error"] = error_msg
                result["explanation"] = self.llm_chain.explain_error(
                    question=question,
                    sql=sql_result["sql"],
                    error=error_msg,
                )
                return result
            
            # 4. SQL'i çalıştır
            try:
                query_results = self.executor.execute_query(
                    sql=sql_result["sql"],
                    validate=False,  # Zaten valide ettik
                )
                
                result["results"] = query_results
                result["success"] = True
                result["metadata"]["row_count"] = len(query_results)
                
                # 5. Sonuçları açıkla
                if explain_results and query_results:
                    result["explanation"] = self.llm_chain.explain_results(
                        question=question,
                        sql=sql_result["sql"],
                        results=query_results,
                    )
                elif not query_results:
                    result["explanation"] = "Sorgunuz için sonuç bulunamadı."
                else:
                    result["explanation"] = sql_result.get("explanation", "")
                
            except Exception as e:
                result["error"] = str(e)
                result["explanation"] = self.llm_chain.explain_error(
                    question=question,
                    sql=sql_result["sql"],
                    error=str(e),
                )
                logger.error("Query execution failed", error=str(e))
            
        except Exception as e:
            result["error"] = str(e)
            result["explanation"] = f"Beklenmeyen bir hata oluştu: {str(e)}"
            logger.error("Query processing failed", error=str(e))
        
        return result
    
    def _get_schema(self) -> str:
        """
        Veritabanı schema'sını al (cache'den veya yeniden)
        
        Returns:
            LLM için formatlanmış schema
        """
        if self._cached_schema is None:
            logger.info("Loading database schema")
            self._cached_schema = self.schema_manager.get_schema_for_llm()
        
        return self._cached_schema
    
    def refresh_schema(self):
        """Schema cache'ini yenile"""
        logger.info("Refreshing schema cache")
        self.schema_manager.clear_cache()
        self._cached_schema = None
    
    def test_query(self, question: str) -> Dict[str, Any]:
        """
        Sorguyu test et (çalıştırmadan)
        
        Args:
            question: Kullanıcının sorusu
        
        Returns:
            Test sonuçları
        """
        logger.info("Testing query", question=question)
        
        schema = self._get_schema()
        sql_result = self.llm_chain.generate_sql(
            question=question,
            schema=schema,
            include_examples=True,
        )
        
        if not sql_result.get("sql"):
            return {
                "valid": False,
                "error": "SQL oluşturulamadı",
                "sql": None,
            }
        
        # Validasyon testi
        test_result = self.executor.test_query(sql_result["sql"])
        test_result["generated_sql"] = sql_result["sql"]
        test_result["llm_confidence"] = sql_result.get("confidence", 0.0)
        test_result["llm_explanation"] = sql_result.get("explanation", "")
        
        return test_result
    
    def get_schema_info(self) -> Dict[str, Any]:
        """
        Veritabanı schema bilgisini al
        
        Returns:
            Schema metadata
        """
        return self.schema_manager.get_full_schema(include_samples=True)
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Belirli bir tablo hakkında bilgi al
        
        Args:
            table_name: Tablo adı
        
        Returns:
            Tablo bilgileri
        """
        schema = self.get_schema_info()
        return schema.get(table_name, {})
    
    def suggest_questions(self, count: int = 5) -> List[str]:
        """
        Örnek sorular öner
        
        Args:
            count: Öneri sayısı
        
        Returns:
            Örnek soru listesi
        """
        # Basit öneriler (gelişmiş versiyonda LLM ile dinamik üretilebilir)
        suggestions = [
            "Kaç müşterimiz var?",
            "En pahalı 5 ürünü göster",
            "Hangi şehirden en fazla sipariş geldi?",
            "En çok satan ürünler hangileri?",
            "İstanbul'dan kaç müşteri var?",
            "Toplam sipariş tutarı ne kadar?",
            "Bugün kaç sipariş alındı?",
            "Stokta olmayan ürünler hangileri?",
            "Ortalama sipariş tutarı nedir?",
            "En çok sipariş veren müşteri kim?",
        ]
        
        return suggestions[:count]
    
    def interactive_query(self, question: str) -> str:
        """
        İnteraktif mod için basitleştirilmiş sorgu
        
        Args:
            question: Kullanıcının sorusu
        
        Returns:
            Formatlanmış yanıt metni
        """
        result = self.query(question, explain_results=True)
        
        if not result["success"]:
            return f"❌ Hata: {result.get('explanation', result.get('error', 'Bilinmeyen hata'))}"
        
        response = f"✅ Sorgu başarılı!\n\n"
        
        if result.get("explanation"):
            response += f"{result['explanation']}\n\n"
        
        if result.get("metadata", {}).get("row_count", 0) > 0:
            response += f"📊 {result['metadata']['row_count']} sonuç bulundu.\n"
        
        return response
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Veritabanı istatistiklerini al
        
        Returns:
            İstatistik bilgileri
        """
        schema = self.get_schema_info()
        
        stats = {
            "table_count": len(schema),
            "tables": {},
        }
        
        for table_name, table_info in schema.items():
            stats["tables"][table_name] = {
                "row_count": table_info.get("row_count", 0),
                "column_count": len(table_info.get("columns", [])),
                "has_foreign_keys": len(table_info.get("foreign_keys", [])) > 0,
            }
        
        return stats

