"""Veritabanını otomatik olarak oluştur ve kurulum yap"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def create_database():
    """Veritabanını oluştur"""
    # Önce postgres veritabanına bağlan
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD'),
        database='postgres'  # postgres default veritabanı
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Veritabanını oluştur
    db_name = os.getenv('DB_NAME', 'ecommerce_db')
    
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        print(f"✓ Eski {db_name} veritabanı silindi (varsa)")
        
        cursor.execute(f"CREATE DATABASE {db_name} WITH ENCODING 'UTF8';")
        print(f"✓ {db_name} veritabanı oluşturuldu")
    except Exception as e:
        print(f"✗ Hata: {e}")
    finally:
        cursor.close()
        conn.close()

def setup_schema():
    """SQL dosyasını çalıştır"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'ecommerce_db')
    )
    cursor = conn.cursor()
    
    # SQL dosyasını oku ve çalıştır
    sql_file = 'examples/sample_db.sql'
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        cursor.execute(sql_content)
        conn.commit()
        print(f"✓ {sql_file} başarıyla çalıştırıldı")
        
        # Kontrol et
        cursor.execute("SELECT COUNT(*) FROM customers;")
        customer_count = cursor.fetchone()[0]
        print(f"✓ {customer_count} müşteri eklendi")
        
        cursor.execute("SELECT COUNT(*) FROM products;")
        product_count = cursor.fetchone()[0]
        print(f"✓ {product_count} ürün eklendi")
        
        cursor.execute("SELECT COUNT(*) FROM orders;")
        order_count = cursor.fetchone()[0]
        print(f"✓ {order_count} sipariş eklendi")
        
    except Exception as e:
        print(f"✗ Hata: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("🚀 Veritabanı kurulumu başlıyor...\n")
    
    try:
        create_database()
        setup_schema()
        print("\n✅ Veritabanı kurulumu tamamlandı!")
        print("\nŞimdi çalıştırabilirsiniz: python main.py")
    except Exception as e:
        print(f"\n❌ Kurulum başarısız: {e}")
        print("\nLütfen .env dosyanızı kontrol edin:")
        print("- DB_HOST")
        print("- DB_PORT")
        print("- DB_USER")
        print("- DB_PASSWORD")

