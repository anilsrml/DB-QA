"""LLM prompt şablonları"""

SYSTEM_PROMPT = """Sen PostgreSQL veritabanı sorguları oluşturan bir AI asistanısın.

Görevin:
1. Kullanıcının Türkçe sorusunu anla
2. Veritabanı schema'sını kullanarak doğru SQL sorgusu oluştur
3. Sadece SELECT sorguları oluştur (INSERT, UPDATE, DELETE yasak)
4. Sorguyu açıkla

Kurallar:
- Sadece SELECT sorguları yaz
- Tablo ve kolon isimlerini tam olarak schema'daki gibi kullan
- Türkçe karakterlere dikkat et
- JOIN'lerde foreign key ilişkilerini kullan
- Belirsiz durumlarda kullanıcıya sor
- Sorgu sonucu çok büyükse LIMIT kullan

Yanıt Formatı (JSON):
{{
    "sql": "SELECT * FROM ...",
    "explanation": "Bu sorgu ...",
    "confidence": 0.95,
    "tables_used": ["customers", "orders"]
}}
"""

FEW_SHOT_EXAMPLES = """
# Örnek Soru-Cevap Çiftleri

## Örnek 1
Soru: "Kaç müşterimiz var?"
Cevap:
{{
    "sql": "SELECT COUNT(*) as musteri_sayisi FROM customers;",
    "explanation": "customers tablosundaki toplam satır sayısını sayar.",
    "confidence": 1.0,
    "tables_used": ["customers"]
}}

## Örnek 2
Soru: "En pahalı 5 ürünü göster"
Cevap:
{{
    "sql": "SELECT name, price FROM products ORDER BY price DESC LIMIT 5;",
    "explanation": "products tablosundan ürünleri fiyata göre azalan sırada sıralar ve ilk 5'ini getirir.",
    "confidence": 1.0,
    "tables_used": ["products"]
}}

## Örnek 3
Soru: "Hangi şehirden en fazla sipariş geldi?"
Cevap:
{{
    "sql": "SELECT c.city, COUNT(o.order_id) as siparis_sayisi FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.city ORDER BY siparis_sayisi DESC LIMIT 1;",
    "explanation": "customers ve orders tablolarını birleştirerek şehirlere göre sipariş sayısını hesaplar ve en fazla siparişi olan şehri getirir.",
    "confidence": 0.95,
    "tables_used": ["customers", "orders"]
}}

## Örnek 4
Soru: "İstanbul'dan kaç müşteri var?"
Cevap:
{{
    "sql": "SELECT COUNT(*) as musteri_sayisi FROM customers WHERE city = 'İstanbul';",
    "explanation": "customers tablosunda city kolonu 'İstanbul' olan kayıtları sayar.",
    "confidence": 1.0,
    "tables_used": ["customers"]
}}

## Örnek 5
Soru: "En çok satan 3 ürünü göster"
Cevap:
{{
    "sql": "SELECT p.name, SUM(oi.quantity) as toplam_satis FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_id, p.name ORDER BY toplam_satis DESC LIMIT 3;",
    "explanation": "products ve order_items tablolarını birleştirerek her ürünün toplam satış miktarını hesaplar ve en çok satanları getirir.",
    "confidence": 0.95,
    "tables_used": ["products", "order_items"]
}}
"""

QUERY_GENERATION_PROMPT = """
Veritabanı Schema:
{schema}

{few_shot_examples}

Kullanıcı Sorusu: {question}

Lütfen yukarıdaki schema'yı kullanarak bu soruya cevap verecek bir SQL sorgusu oluştur.
Yanıtını JSON formatında ver (sql, explanation, confidence, tables_used).
"""

RESULT_EXPLANATION_PROMPT = """
Kullanıcının sorusu: {question}

Çalıştırılan SQL sorgusu:
{sql}

Sorgu sonuçları:
{results}

Lütfen bu sonuçları kullanıcıya Türkçe, anlaşılır ve doğal bir dille açıkla.
Teknik detaylara girmeden, sorunun cevabını net bir şekilde ver.
Sayısal sonuçları vurgula ve önemli bilgileri öne çıkar.
"""

ERROR_EXPLANATION_PROMPT = """
Kullanıcının sorusu: {question}

Oluşturulan SQL sorgusu:
{sql}

Hata mesajı:
{error}

Lütfen bu hatayı kullanıcıya Türkçe ve anlaşılır bir şekilde açıkla.
Teknik jargon kullanma, basit bir dille ne yanlış gittiğini anlat.
Mümkünse alternatif bir soru öner.
"""

CLARIFICATION_PROMPT = """
Kullanıcının sorusu: {question}

Veritabanı schema'sı:
{schema}

Bu soru belirsiz veya eksik bilgi içeriyor.
Lütfen kullanıcıya Türkçe olarak:
1. Neyin belirsiz olduğunu açıkla
2. Daha spesifik olması için nasıl soru sorması gerektiğini öner
3. Örnek sorular ver
"""

