#  PostgreSQL Doğal Dil Sorgu Agent Sistemi

Proje Tanımı

Bu proje, kullanıcıların PostgreSQL veritabanlarını Türkçe doğal dil kullanarak sorgulamasını sağlayan, yapay zeka destekli bir doğal dil sorgu agent sistemidir. Kullanıcılar SQL bilmeden soru sorabilir; sistem bu soruları analiz eder, güvenli SQL sorguları üretir, veritabanında çalıştırır ve sonuçları anlaşılır bir Türkçe açıklama ile sunar.

Proje, LLM tabanlı agent mimarisi, veritabanı güvenliği ve doğal dil işleme konularını gerçekçi bir senaryo üzerinden birleştiren, üretime yakın bir örnek olarak tasarlanmıştır.

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
# LLM Provider: "ollama" veya "gemini"
LLM_PROVIDER=ollama

# Ollama Ayarları
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=kullanılacak-model

# Gemini (opsiyonel)
# GOOGLE_API_KEY=...

# PostgreSQL Bağlantı Bilgilerini Girin. Database'i bağlayın.
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

### Bağlantı Testi

```bash
python main.py test
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


**Not**: Bu sistem sadece SELECT sorguları çalıştırır. Veri değiştirme, silme veya veritabanı yapısını değiştirme işlemleri güvenlik nedeniyle engellenmiştir.
