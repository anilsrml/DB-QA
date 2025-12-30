-- PostgreSQL E-Ticaret Örnek Veritabanı
-- Bu veritabanı, doğal dil sorgu sistemini test etmek için tasarlanmıştır

-- Veritabanını oluştur (opsiyonel)
-- CREATE DATABASE ecommerce_db;

-- Müşteriler tablosu
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(50),
    registration_date DATE DEFAULT CURRENT_DATE,
    is_active BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE customers IS 'Müşteri bilgilerini içerir';
COMMENT ON COLUMN customers.name IS 'Müşterinin tam adı';
COMMENT ON COLUMN customers.city IS 'Müşterinin bulunduğu şehir';

-- Kategoriler tablosu
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    parent_category_id INTEGER REFERENCES categories(category_id)
);

COMMENT ON TABLE categories IS 'Ürün kategorileri';
COMMENT ON COLUMN categories.parent_category_id IS 'Üst kategori (alt kategori yapısı için)';

-- Ürünler tablosu
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE products IS 'Satışa sunulan ürünler';
COMMENT ON COLUMN products.stock_quantity IS 'Stok miktarı';

-- Siparişler tablosu
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    shipping_address TEXT
);

COMMENT ON TABLE orders IS 'Müşteri siparişleri';
COMMENT ON COLUMN orders.status IS 'Sipariş durumu: pending, processing, shipped, delivered, cancelled';

-- Sipariş detayları tablosu
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0)
);

COMMENT ON TABLE order_items IS 'Sipariş kalemlerinin detayları';

-- İndeksler (performans için)
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);

-- Örnek veriler ekle

-- Kategoriler
INSERT INTO categories (name, description) VALUES
('Elektronik', 'Elektronik cihazlar ve aksesuarlar'),
('Giyim', 'Kadın, erkek ve çocuk giyim'),
('Ev & Yaşam', 'Ev eşyaları ve dekorasyon'),
('Kitap', 'Kitaplar ve dergiler'),
('Spor', 'Spor malzemeleri ve ekipmanları')
ON CONFLICT (name) DO NOTHING;

-- Alt kategoriler
INSERT INTO categories (name, description, parent_category_id) VALUES
('Telefon', 'Akıllı telefonlar', 1),
('Bilgisayar', 'Dizüstü ve masaüstü bilgisayarlar', 1),
('Erkek Giyim', 'Erkek kıyafetleri', 2),
('Kadın Giyim', 'Kadın kıyafetleri', 2)
ON CONFLICT (name) DO NOTHING;

-- Müşteriler
INSERT INTO customers (name, email, city, registration_date) VALUES
('Ahmet Yılmaz', 'ahmet.yilmaz@email.com', 'İstanbul', '2024-01-15'),
('Ayşe Demir', 'ayse.demir@email.com', 'Ankara', '2024-02-20'),
('Mehmet Kaya', 'mehmet.kaya@email.com', 'İzmir', '2024-03-10'),
('Fatma Şahin', 'fatma.sahin@email.com', 'İstanbul', '2024-04-05'),
('Ali Öztürk', 'ali.ozturk@email.com', 'Bursa', '2024-05-12'),
('Zeynep Aydın', 'zeynep.aydin@email.com', 'Antalya', '2024-06-18'),
('Mustafa Çelik', 'mustafa.celik@email.com', 'İstanbul', '2024-07-22'),
('Elif Yıldız', 'elif.yildiz@email.com', 'Ankara', '2024-08-30'),
('Can Arslan', 'can.arslan@email.com', 'İzmir', '2024-09-14'),
('Selin Koç', 'selin.koc@email.com', 'İstanbul', '2024-10-25')
ON CONFLICT (email) DO NOTHING;

-- Ürünler
INSERT INTO products (name, category_id, price, stock_quantity, description) VALUES
('iPhone 15 Pro', 6, 7343.33, 25, 'Apple iPhone 15 Pro 256GB'),
('Samsung Galaxy S24', 6, 38999.00, 30, 'Samsung Galaxy S24 128GB'),
('MacBook Air M2', 7, 52999.00, 15, 'Apple MacBook Air M2 13 inç'),
('Dell XPS 13', 7, 42999.00, 20, 'Dell XPS 13 Dizüstü Bilgisayar'),
('Erkek Kot Pantolon', 8, 299.90, 100, 'Slim fit erkek kot pantolon'),
('Kadın Elbise', 9, 96000.90, 75, 'Yazlık kadın elbise'),
('Spor Ayakkabı', 5, 899.90, 50, 'Koşu ayakkabısı'),
('Kitap: Suç ve Ceza', 4, 89.90, 200, 'Dostoyevski - Suç ve Ceza'),
('Kahve Makinesi', 3, 1299.00, 40, 'Otomatik kahve makinesi'),
('Yoga Matı', 5, 199.90, 60, 'Kaymaz yoga matı')
ON CONFLICT DO NOTHING;

-- Siparişler ve sipariş kalemleri
DO $$
DECLARE
    order1_id INTEGER;
    order2_id INTEGER;
    order3_id INTEGER;
    order4_id INTEGER;
    order5_id INTEGER;
BEGIN
    -- Sipariş 1
    INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
    VALUES (1, '2024-11-01 10:30:00', 46898.90, 'delivered', 'İstanbul, Kadıköy')
    RETURNING order_id INTO order1_id;
    
    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (order1_id, 1, 1, 45999.00),
    (order1_id, 7, 1, 899.90);
    
    -- Sipariş 2
    INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
    VALUES (2, '2024-11-05 14:20:00', 53898.90, 'delivered', 'Ankara, Çankaya')
    RETURNING order_id INTO order2_id;
    
    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (order2_id, 3, 1, 52999.00),
    (order2_id, 5, 3, 299.90);
    
    -- Sipariş 3
    INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
    VALUES (3, '2024-11-10 09:15:00', 1399.80, 'shipped', 'İzmir, Karşıyaka')
    RETURNING order_id INTO order3_id;
    
    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (order3_id, 9, 1, 1299.00),
    (order3_id, 8, 1, 89.90),
    (order3_id, 10, 1, 199.90);
    
    -- Sipariş 4
    INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
    VALUES (1, '2024-11-15 16:45:00', 38999.00, 'processing', 'İstanbul, Kadıköy')
    RETURNING order_id INTO order4_id;
    
    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (order4_id, 2, 1, 38999.00);
    
    -- Sipariş 5
    INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
    VALUES (4, '2024-11-20 11:30:00', 1799.60, 'delivered', 'İstanbul, Beşiktaş')
    RETURNING order_id INTO order5_id;
    
    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (order5_id, 6, 2, 449.90),
    (order5_id, 7, 1, 899.90);
    
    -- Daha fazla sipariş
    INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
    VALUES 
    (5, '2024-11-22 10:00:00', 42999.00, 'delivered', 'Bursa, Nilüfer'),
    (6, '2024-11-25 15:30:00', 2699.70, 'delivered', 'Antalya, Muratpaşa'),
    (7, '2024-11-28 12:15:00', 45999.00, 'processing', 'İstanbul, Şişli'),
    (8, '2024-12-01 09:45:00', 899.80, 'pending', 'Ankara, Keçiören'),
    (9, '2024-12-05 14:20:00', 1499.80, 'shipped', 'İzmir, Bornova');
    
    -- Son siparişlerin kalemlerini ekle
    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    SELECT 
        o.order_id,
        CASE 
            WHEN o.customer_id = 5 THEN 4
            WHEN o.customer_id = 6 THEN 5
            WHEN o.customer_id = 7 THEN 1
            WHEN o.customer_id = 8 THEN 8
            WHEN o.customer_id = 9 THEN 9
        END,
        CASE 
            WHEN o.customer_id = 6 THEN 9
            WHEN o.customer_id = 8 THEN 10
            ELSE 1
        END,
        p.price
    FROM orders o
    JOIN products p ON p.product_id = CASE 
        WHEN o.customer_id = 5 THEN 4
        WHEN o.customer_id = 6 THEN 5
        WHEN o.customer_id = 7 THEN 1
        WHEN o.customer_id = 8 THEN 8
        WHEN o.customer_id = 9 THEN 9
    END
    WHERE o.order_id > order5_id;
    
END $$;

-- Veritabanı istatistiklerini güncelle
ANALYZE customers;
ANALYZE categories;
ANALYZE products;
ANALYZE orders;
ANALYZE order_items;
