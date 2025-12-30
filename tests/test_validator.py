"""SQL Validator testleri"""

import pytest
from src.validation.sql_validator import SQLValidator, ValidationError


class TestSQLValidator:
    """SQL Validator test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.validator = SQLValidator(strict_mode=True)
    
    def test_valid_select_query(self):
        """Geçerli SELECT sorgusu testi"""
        sql = "SELECT * FROM customers;"
        is_valid, error = self.validator.validate(sql)
        assert is_valid is True
        assert error is None
    
    def test_select_with_where(self):
        """WHERE ile SELECT testi"""
        sql = "SELECT name, email FROM customers WHERE city = 'İstanbul';"
        is_valid, error = self.validator.validate(sql)
        assert is_valid is True
    
    def test_select_with_join(self):
        """JOIN ile SELECT testi"""
        sql = """
            SELECT c.name, o.order_date 
            FROM customers c 
            JOIN orders o ON c.customer_id = o.customer_id;
        """
        is_valid, error = self.validator.validate(sql)
        assert is_valid is True
    
    def test_insert_forbidden(self):
        """INSERT yasağı testi"""
        sql = "INSERT INTO customers (name) VALUES ('Test');"
        is_valid, error = self.validator.validate(sql)
        assert is_valid is False
        assert "INSERT" in error
    
    def test_update_forbidden(self):
        """UPDATE yasağı testi"""
        sql = "UPDATE customers SET name = 'Test' WHERE id = 1;"
        is_valid, error = self.validator.validate(sql)
        assert is_valid is False
        assert "UPDATE" in error
    
    def test_delete_forbidden(self):
        """DELETE yasağı testi"""
        sql = "DELETE FROM customers WHERE id = 1;"
        is_valid, error = self.validator.validate(sql)
        assert is_valid is False
        assert "DELETE" in error
    
    def test_drop_forbidden(self):
        """DROP yasağı testi"""
        sql = "DROP TABLE customers;"
        is_valid, error = self.validator.validate(sql)
        assert is_valid is False
        assert "DROP" in error
    
    def test_query_too_long(self):
        """Çok uzun sorgu testi"""
        sql = "SELECT * FROM customers WHERE " + " OR ".join([f"id = {i}" for i in range(1000)])
        is_valid, error = self.validator.validate(sql)
        assert is_valid is False
        assert "uzun" in error.lower()
    
    def test_sanitize_sql(self):
        """SQL temizleme testi"""
        sql = "  SELECT   *   FROM   customers  "
        sanitized = self.validator.sanitize_sql(sql)
        assert "SELECT" in sanitized
        assert "FROM" in sanitized
        assert "customers" in sanitized
    
    def test_extract_table_names(self):
        """Tablo ismi çıkarma testi"""
        sql = "SELECT * FROM customers JOIN orders ON customers.id = orders.customer_id"
        tables = self.validator.extract_table_names(sql)
        # En az bir tablo bulmalı
        assert len(tables) > 0


class TestSQLValidatorStrictMode:
    """Strict mode testleri"""
    
    def test_too_many_joins(self):
        """Çok fazla JOIN testi"""
        validator = SQLValidator(strict_mode=True)
        
        # 11 JOIN oluştur (limit 10)
        joins = " ".join([f"JOIN table{i} ON table{i-1}.id = table{i}.id" for i in range(1, 12)])
        sql = f"SELECT * FROM table0 {joins}"
        
        is_valid, error = self.validator.validate(sql)
        # Karmaşıklık limiti aşılmalı
        assert is_valid is False or "JOIN" in str(error)

