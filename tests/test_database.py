"""Database modülü testleri"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.database.connection import DatabaseConnection
from src.database.schema_manager import SchemaManager


class TestDatabaseConnection:
    """DatabaseConnection test sınıfı"""
    
    @patch('src.database.connection.psycopg2.connect')
    def test_connect_success(self, mock_connect):
        """Başarılı bağlantı testi"""
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        conn = db.connect()
        
        assert conn is not None
        mock_connect.assert_called_once()
    
    @patch('src.database.connection.psycopg2.connect')
    def test_disconnect(self, mock_connect):
        """Bağlantı kapatma testi"""
        mock_conn = Mock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        db.connect()
        db.disconnect()
        
        mock_conn.close.assert_called_once()
    
    @patch('src.database.connection.psycopg2.connect')
    def test_context_manager(self, mock_connect):
        """Context manager testi"""
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        with DatabaseConnection() as db:
            assert db is not None
        
        # Bağlantı kapatılmalı
        mock_conn.close.assert_called()


class TestSchemaManager:
    """SchemaManager test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.mock_db = Mock(spec=DatabaseConnection)
    
    def test_initialization(self):
        """Schema manager başlatma testi"""
        schema_manager = SchemaManager(self.mock_db)
        assert schema_manager.db is self.mock_db
        assert schema_manager._schema_cache is None
    
    @patch.object(DatabaseConnection, 'get_cursor')
    def test_get_all_tables(self, mock_cursor):
        """Tablo listesi alma testi"""
        # Mock cursor ve sonuçlar
        mock_cursor_obj = MagicMock()
        mock_cursor_obj.__enter__.return_value = mock_cursor_obj
        mock_cursor_obj.__exit__.return_value = None
        mock_cursor_obj.fetchall.return_value = [
            {'table_name': 'customers'},
            {'table_name': 'orders'},
        ]
        
        self.mock_db.get_cursor.return_value = mock_cursor_obj
        
        schema_manager = SchemaManager(self.mock_db)
        tables = schema_manager.get_all_tables()
        
        assert len(tables) == 2
        assert 'customers' in tables
        assert 'orders' in tables
    
    def test_clear_cache(self):
        """Cache temizleme testi"""
        schema_manager = SchemaManager(self.mock_db)
        schema_manager._schema_cache = {"test": "data"}
        
        schema_manager.clear_cache()
        
        assert schema_manager._schema_cache is None

