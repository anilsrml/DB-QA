#  PostgreSQL Doğal Dil Sorgu Agent Sistemi

PostgreSQL veritabanınıza Türkçe sorular sorun, AI otomatik olarak SQL oluştursun ve çalıştırsın!

##  Gereksinimler

- Python 3.8+
- PostgreSQL 12+
- Google Gemini API Key

##  Kurulum

---
### 1. Projeyi İndirin

```bash
git clone <repo-url>
cd dbq
```

### 2. Virtual Environment Oluşturun

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Çevre Değişkenlerini Ayarlayın

`.env` dosyası oluşturun:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```env
# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# PostgreSQL Bağlantı Bilgileri
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password_here

# Güvenlik Ayarları
MAX_QUERY_TIMEOUT=30
MAX_RESULT_ROWS=1000

# Loglama
LOG_LEVEL=INFO
```

### 5. Örnek Veritabanını Oluşturun (Opsiyonel)

```bash
# PostgreSQL'e bağlanın
psql -U postgres

# Veritabanını oluşturun
CREATE DATABASE ecommerce_db;

# Veritabanına geçin
\c ecommerce_db

# Schema'yı yükleyin
\i examples/sample_db.sql
```

## 📖 Kullanım

### İnteraktif Mod (Önerilen)

```bash
python main.py
```

veya

```bash
python main.py interactive
```

Açılan arayüzde Türkçe sorularınızı yazın:

```
Soru: Kaç müşterimiz var?
Soru: En pahalı 5 ürünü göster
Soru: Hangi şehirden en fazla sipariş geldi?
```

### Tek Sorgu Modu

```bash
python main.py query "Kaç müşterimiz var?"
```

Ham JSON çıktısı için:

```bash
python main.py query "En pahalı ürün hangisi?" --raw
```

### Bağlantı Testi

```bash
python main.py test
```

##  Örnek Kullanım Senaryoları

### Basit Sorgular

```
Kaç müşterimiz var?
Stokta kaç ürün var?
Bugün kaç sipariş alındı?
Hangi kategorilerde ürün satıyoruz?
```

### İstatistik Sorguları

```
Toplam sipariş tutarı ne kadar?
Ortalama sipariş tutarı nedir?
En pahalı ürün hangisi?
Elektronik kategorisindeki ürünlerin ortalama fiyatı nedir?
```

### Filtreleme ve Sıralama

```
İstanbul'dan kaç müşteri var?
Fiyatı 1000 TL'den pahalı ürünleri listele
Teslim edilmiş siparişleri göster
En çok satan 5 ürünü göster
```

### Karmaşık Sorgular

```
Hangi şehirden en fazla sipariş geldi?
En çok sipariş veren 3 müşteriyi göster
Her kategoride kaç ürün var?
Ortalama sipariş tutarının üzerinde sipariş veren müşteriler kimler?
```

## 🛠️ CLI Komutları

İnteraktif modda kullanabileceğiniz özel komutlar:

- `help` - Yardım mesajını göster
- `schema` - Veritabanı yapısını göster
- `stats` - Veritabanı istatistiklerini göster
- `examples` - Örnek sorular listesi
- `clear` - Ekranı temizle
- `exit` veya `quit` - Çıkış

##  Proje Yapısı

```
dbq/
├── src/
│   ├── agent/              # AI Agent modülü
│   │   ├── core.py         # Ana agent logic
│   │   ├── prompts.py      # LLM prompt şablonları
│   │   └── chain.py        # LangChain zincirleri
│   ├── database/           # Veritabanı modülü
│   │   ├── connection.py   # Bağlantı yönetimi
│   │   ├── schema_manager.py  # Schema analizi
│   │   └── executor.py     # Sorgu çalıştırma
│   ├── validation/         # Güvenlik modülü
│   │   ├── sql_validator.py   # SQL validasyonu
│   │   └── rules.py        # Güvenlik kuralları
│   ├── utils/              # Yardımcı araçlar
│   │   ├── logger.py       # Loglama
│   │   └── formatters.py   # Sonuç formatlama
│   ├── config.py           # Konfigürasyon
│   └── cli.py              # CLI arayüzü
├── examples/
│   ├── sample_db.sql       # Örnek veritabanı
│   └── sample_queries.txt  # Örnek sorular
├── tests/                  # Test dosyaları
├── .env.example            # Çevre değişkenleri şablonu
├── requirements.txt        # Python bağımlılıkları
├── main.py                 # Giriş noktası
└── README.md
```

##  Test

```bash
# Tüm testleri çalıştır
pytest

# Coverage ile
pytest --cov=src

# Belirli bir test dosyası
pytest tests/test_agent.py
```

##  Mimari

```
┌─────────────┐
│  Kullanıcı  │
└──────┬──────┘
       │ Türkçe Soru
       ▼
┌─────────────┐
│ CLI Arayüzü │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   AI Agent      │
│  (QueryAgent)   │
└────┬───┬───┬────┘
     │   │   │
     │   │   └──────────┐
     │   │              │
     ▼   ▼              ▼
┌─────────┐  ┌──────────────┐  ┌──────────┐
│ Schema  │  │ SQL Generator│  │Validator │
│ Manager │  │  (Gemini)    │  │          │
└─────────┘  └──────────────┘  └──────────┘
     │              │                │
     │              │                │
     └──────────────┴────────────────┘
                    │
                    ▼
            ┌───────────────┐
            │ Query Executor│
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  PostgreSQL   │
            └───────────────┘
```

## 🔧 Konfigürasyon

### Timeout Ayarları

```python
MAX_QUERY_TIMEOUT=30  # Saniye
```

### Sonuç Limiti

```python
MAX_RESULT_ROWS=1000  # Maksimum satır
```

### LLM Ayarları

```python
# src/agent/core.py içinde
agent = QueryAgent(db_connection, temperature=0.1)
```


**Not**: Bu sistem sadece SELECT sorguları çalıştırır. Veri değiştirme, silme veya veritabanı yapısını değiştirme işlemleri güvenlik nedeniyle engellenmiştir.
