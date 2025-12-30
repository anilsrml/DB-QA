"""Agent modülü testleri"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.agent.core import QueryAgent
from src.agent.chain import LLMChainManager
from src.database.connection import DatabaseConnection


class TestQueryAgent:
    """QueryAgent test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.mock_db = Mock(spec=DatabaseConnection)
    
    @patch('src.agent.core.SchemaManager')
    @patch('src.agent.core.QueryExecutor')
    @patch('src.agent.core.LLMChainManager')
    def test_initialization(self, mock_llm, mock_executor, mock_schema):
        """Agent başlatma testi"""
        agent = QueryAgent(self.mock_db)
        
        assert agent.db is self.mock_db
        assert agent._cached_schema is None
    
    @patch('src.agent.core.SchemaManager')
    @patch('src.agent.core.QueryExecutor')
    @patch('src.agent.core.LLMChainManager')
    def test_suggest_questions(self, mock_llm, mock_executor, mock_schema):
        """Soru önerisi testi"""
        agent = QueryAgent(self.mock_db)
        suggestions = agent.suggest_questions(count=5)
        
        assert len(suggestions) == 5
        assert all(isinstance(q, str) for q in suggestions)


class TestLLMChainManager:
    """LLMChainManager test sınıfı"""
    
    @patch('src.agent.chain.ChatGoogleGenerativeAI')
    def test_initialization(self, mock_gemini):
        """LLM chain başlatma testi"""
        mock_llm = Mock()
        mock_gemini.return_value = mock_llm
        
        chain_manager = LLMChainManager(temperature=0.1)
        
        assert chain_manager.temperature == 0.1
        assert chain_manager.llm is not None
    
    @patch('src.agent.chain.ChatGoogleGenerativeAI')
    def test_parse_json_response(self, mock_gemini):
        """JSON parse testi"""
        mock_llm = Mock()
        mock_gemini.return_value = mock_llm
        
        chain_manager = LLMChainManager()
        
        # Geçerli JSON
        response = '{"sql": "SELECT * FROM customers;", "confidence": 0.95}'
        result = chain_manager._parse_json_response(response)
        
        assert result["sql"] == "SELECT * FROM customers;"
        assert result["confidence"] == 0.95
    
    @patch('src.agent.chain.ChatGoogleGenerativeAI')
    def test_format_results_for_llm(self, mock_gemini):
        """Sonuç formatlama testi"""
        mock_llm = Mock()
        mock_gemini.return_value = mock_llm
        
        chain_manager = LLMChainManager()
        
        results = [
            {"id": 1, "name": "Test 1"},
            {"id": 2, "name": "Test 2"},
        ]
        
        formatted = chain_manager._format_results_for_llm(results, max_rows=10)
        
        assert "Test 1" in formatted
        assert "Test 2" in formatted

