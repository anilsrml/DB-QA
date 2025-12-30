# 📦 Detaylı Kurulum Kılavuzu

Bu kılavuz, PostgreSQL Doğal Dil Sorgu Agent Sistemini adım adım kurmak için hazırlanmıştır.

## 🔧 Ön Gereksinimler

### 1. Python Kurulumu

Python 3.8 veya üzeri gereklidir.

**Kontrol:**
```bash
python --version
```

**İndirme:** [python.org](https://www.python.org/downloads/)

### 2. PostgreSQL Kurulumu

PostgreSQL 12 veya üzeri gereklidir.

**Windows:**
- [PostgreSQL İndir](https://www.postgresql.org/download/windows/)
- Installer'ı çalıştırın ve varsayılan ayarları kullanın
- Şifrenizi not edin!

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Kontrol:**
```bash
psql --version
```

### 3. Google Gemini API Key

1. [Google AI Studio](https://makersuite.google.com/app/apikey)'ya gidin
2. "Create API Key" butonuna tıklayın
3. API key'inizi kopyalayın ve güvenli bir yerde saklayın

## 📥 Proje Kurulumu

### Adım 1: Projeyi İndirin

```bash
# Git ile
git clone <repo-url>
cd dbq

# Veya ZIP olarak indirip çıkarın
```

### Adım 2: Virtual Environment Oluşturun

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Başarılı olursa komut satırında `(venv)` görünür.

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Bu işlem birkaç dakika sürebilir.

### Adım 4: Çevre Değişkenlerini Ayarlayın

1. `.env.example` dosyasını kopyalayın:

**Windows:**
```bash
copy .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

2. `.env` dosyasını bir metin editörü ile açın ve düzenleyin:

```env
# Google Gemini API Key (zorunlu)
GOOGLE_API_KEY=AIzaSy...  # Buraya kendi API key'inizi yazın

# PostgreSQL Bağlantı Bilgileri
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password_here  # PostgreSQL şifrenizi yazın

# Güvenlik Ayarları (varsayılan değerler)
MAX_QUERY_TIMEOUT=30
MAX_RESULT_ROWS=1000

# Loglama
LOG_LEVEL=INFO
```

## 🗄️ Veritabanı Kurulumu

### Seçenek 1: Örnek Veritabanını Kullanın (Önerilen)

1. PostgreSQL'e bağlanın:

**Windows:**
```bash
psql -U postgres
```

**Linux/macOS:**
```bash
sudo -u postgres psql
```

2. Şifrenizi girin

3. Veritabanını oluşturun:
```sql
CREATE DATABASE ecommerce_db;
\c ecommerce_db
```

4. Schema'yı yükleyin:

**Windows:**
```sql
\i 'C:/Users/YourUser/Desktop/dbq/examples/sample_db.sql'
```

**Linux/macOS:**
```sql
\i '/path/to/dbq/examples/sample_db.sql'
```

5. Kontrol edin:
```sql
\dt
SELECT COUNT(*) FROM customers;
```

6. Çıkış:
```sql
\q
```

### Seçenek 2: Mevcut Veritabanınızı Kullanın

`.env` dosyasında kendi veritabanı bilgilerinizi yazın:

```env
DB_HOST=your_host
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
```

## ✅ Kurulum Testi

1. Bağlantıyı test edin:

```bash
python main.py test
```

**Başarılı çıktı:**
```
Veritabanı bağlantısı test ediliyor...
✓ Bağlantı başarılı!

Toplam 5 tablo bulundu.
```

**Hata alırsanız:**
- `.env` dosyanızı kontrol edin
- PostgreSQL'in çalıştığından emin olun
- Şifrenizin doğru olduğunu kontrol edin

2. İlk sorguyu çalıştırın:

```bash
python main.py query "Kaç müşterimiz var?"
```

## 🚀 Kullanıma Başlayın

### İnteraktif Mod

```bash
python main.py
```

veya

```bash
python main.py interactive
```

### Tek Sorgu

```bash
python main.py query "En pahalı ürün hangisi?"
```

## 🐛 Sık Karşılaşılan Sorunlar

### Sorun 1: ModuleNotFoundError

**Hata:**
```
ModuleNotFoundError: No module named 'langchain'
```

**Çözüm:**
```bash
pip install -r requirements.txt
```

### Sorun 2: PostgreSQL Bağlantı Hatası

**Hata:**
```
could not connect to server
```

**Çözüm:**
1. PostgreSQL'in çalıştığını kontrol edin:
   ```bash
   # Windows
   services.msc
   # PostgreSQL servisi çalışıyor mu?
   
   # Linux
   sudo systemctl status postgresql
   ```

2. `.env` dosyanızı kontrol edin
3. Şifrenizi doğrulayın

### Sorun 3: API Key Hatası

**Hata:**
```
Failed to initialize Gemini LLM
```

**Çözüm:**
1. `GOOGLE_API_KEY` değişkenini kontrol edin
2. API key'in geçerli olduğundan emin olun
3. [Google AI Studio](https://makersuite.google.com/app/apikey)'da yeni key oluşturun

### Sorun 4: psycopg2 Kurulum Hatası

**Hata:**
```
Error: pg_config executable not found
```

**Çözüm (Windows):**
```bash
pip install psycopg2-binary
```

**Çözüm (Linux):**
```bash
sudo apt-get install libpq-dev python3-dev
pip install psycopg2
```

### Sorun 5: Encoding Hatası

**Hata:**
```
UnicodeDecodeError
```

**Çözüm:**
`.env` dosyanızın UTF-8 encoding ile kaydedildiğinden emin olun.

## 🔄 Güncelleme

Projeyi güncellemek için:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🧹 Temizlik

Virtual environment'ı kaldırmak için:

```bash
# Önce deactivate edin
deactivate

# Sonra venv klasörünü silin
# Windows
rmdir /s venv

# Linux/macOS
rm -rf venv
```

## 📞 Yardım

Sorun yaşıyorsanız:

1. README.md dosyasını okuyun
2. GitHub Issues'da arama yapın
3. Yeni issue açın

## ✨ İlk Adımlar

Kurulum tamamlandıktan sonra:

1. `python main.py` ile başlayın
2. `help` yazarak komutları görün
3. `examples` ile örnek sorular görün
4. `schema` ile veritabanı yapısını inceleyin
5. Kendi sorularınızı sormaya başlayın!

**Örnek İlk Sorular:**
```
Kaç müşterimiz var?
En pahalı ürün hangisi?
Hangi şehirden en fazla sipariş geldi?
```

Başarılar! 🎉

