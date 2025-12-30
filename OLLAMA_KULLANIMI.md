# 🦙 Ollama ile Lokal Model Kullanımı

Bu kılavuz, projeyi Ollama ile lokal modeller kullanarak çalıştırmanızı sağlar.

## 🎯 Avantajlar

✅ **Tamamen Lokal** - İnternet bağlantısı gerekmez  
✅ **Ücretsiz** - API key gerekmez  
✅ **Gizlilik** - Verileriniz dışarı çıkmaz  
✅ **Hızlı** - Lokal çalıştığı için hızlı  
✅ **Çoklu Model** - Mistral, Llama, Phi, vs.

## 📥 Adım 1: Ollama Kurulumu

### Windows

1. [Ollama İndir](https://ollama.ai/download/windows)
2. `OllamaSetup.exe` dosyasını çalıştırın
3. Kurulum otomatik tamamlanacak
4. Ollama arka planda çalışmaya başlayacak

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### macOS

```bash
brew install ollama
```

### Kurulumu Kontrol Edin

```powershell
ollama --version
```

## 🤖 Adım 2: Model İndirme

### Önerilen Modeller

```powershell
# Mistral (Önerilen - Hızlı ve iyi)
ollama pull mistral

# Llama 3.2 (Daha güçlü)
ollama pull llama3.2

# Llama 3.2 3B (Daha hafif, hızlı)
ollama pull llama3.2:3b

# Phi 3 (Microsoft - Hafif)
ollama pull phi3

# Gemma 2 (Google - Orta)
ollama pull gemma2
```

### Model Listesini Görüntüleme

```powershell
ollama list
```

**Çıktı:**
```
NAME              ID              SIZE      MODIFIED
mistral:latest    abc123...       4.1 GB    2 days ago
llama3.2:latest   def456...       2.0 GB    1 day ago
```

## ⚙️ Adım 3: Proje Konfigürasyonu

### .env Dosyasını Düzenleyin

```powershell
notepad .env
```

Şu satırları ekleyin/düzenleyin:

```env
# LLM Provider: "ollama" veya "gemini"
LLM_PROVIDER=ollama

# Ollama Ayarları
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Gemini artık gerekli değil (opsiyonel)
# GOOGLE_API_KEY=...

# PostgreSQL ayarları (değişmedi)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password_here

MAX_QUERY_TIMEOUT=30
MAX_RESULT_ROWS=1000
LOG_LEVEL=INFO
```

## 🚀 Adım 4: Projeyi Çalıştırın

```powershell
# Test edin
python main.py test

# Çalıştırın
python main.py
```

## 🔄 Model Değiştirme

Farklı modeller denemek için `.env` dosyasını düzenleyin:

```env
# Mistral kullan
OLLAMA_MODEL=mistral

# Llama 3.2 kullan
OLLAMA_MODEL=llama3.2

# Llama 3.2 3B kullan (daha hızlı)
OLLAMA_MODEL=llama3.2:3b

# Phi 3 kullan
OLLAMA_MODEL=phi3
```

Değiştirdikten sonra projeyi yeniden başlatın.

## 📊 Model Karşılaştırması

| Model | Boyut | Hız | Kalite | RAM |
|-------|-------|-----|--------|-----|
| **mistral** | 4.1 GB | ⚡⚡⚡ | 🧠🧠🧠 | 8 GB |
| **llama3.2** | 2.0 GB | ⚡⚡ | 🧠🧠🧠🧠 | 8 GB |
| **llama3.2:3b** | 2.0 GB | ⚡⚡⚡⚡ | 🧠🧠 | 4 GB |
| **phi3** | 2.3 GB | ⚡⚡⚡ | 🧠🧠🧠 | 4 GB |
| **gemma2** | 5.4 GB | ⚡⚡ | 🧠🧠🧠 | 8 GB |

## 🎯 Hangi Modeli Seçmeliyim?

### Bilgisayarınız Güçlüyse (16GB+ RAM)
```env
OLLAMA_MODEL=llama3.2
```
En iyi kalite, orta hız.

### Hız Öncelikliyse
```env
OLLAMA_MODEL=llama3.2:3b
```
veya
```env
OLLAMA_MODEL=mistral
```

### RAM Sınırlıysa (8GB)
```env
OLLAMA_MODEL=phi3
```

### Türkçe İçin En İyisi
```env
OLLAMA_MODEL=mistral
```
Mistral, Türkçe'de çok iyi performans gösterir.

## 🔧 Sorun Giderme

### Hata: "Ollama connection refused"

**Çözüm:** Ollama çalışmıyor

```powershell
# Windows'ta Ollama'yı başlat
ollama serve
```

Yeni bir terminal açın ve projeyi çalıştırın.

### Hata: "Model not found"

**Çözüm:** Model indirilmemiş

```powershell
ollama pull mistral
```

### Hata: "Out of memory"

**Çözüm:** Daha küçük bir model kullanın

```env
OLLAMA_MODEL=llama3.2:3b
```

### Ollama Çalışıyor mu Kontrol

```powershell
curl http://localhost:11434
```

**Beklenen çıktı:**
```
Ollama is running
```

## 🌐 Gemini'ye Geri Dönme

Ollama yerine tekrar Gemini kullanmak isterseniz:

```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_api_key_here
```

## 📈 Performans İpuçları

1. **GPU Kullanımı**: Ollama otomatik GPU kullanır (NVIDIA/AMD)
2. **RAM**: Model boyutundan 2x RAM olmalı
3. **İlk Sorgu**: İlk sorgu yavaş olabilir (model yükleniyor)
4. **Sonraki Sorgular**: Çok hızlı (model bellekte)

## 🎨 Örnek Kullanım

```
Soru: Kaç müşterimiz var?

[Ollama - Mistral]
✅ Başarılı!

SQL: SELECT COUNT(*) as musteri_sayisi FROM customers;

Veritabanında toplam 10 müşteri bulunmaktadır.

Güven: 95% | Satır: 1
⚡ Tamamen lokal çalıştı - İnternet kullanılmadı!
```

## 🆚 Ollama vs Gemini

| Özellik | Ollama | Gemini |
|---------|--------|--------|
| **Maliyet** | Ücretsiz | API limiti var |
| **İnternet** | Gerekmez | Gerekir |
| **Gizlilik** | %100 lokal | Cloud'a gider |
| **Hız** | Çok hızlı | Orta (ağa bağlı) |
| **Kalite** | İyi-Çok iyi | Mükemmel |
| **Kurulum** | Kolay | Sadece API key |

## 🎯 Sonuç

Ollama ile:
- ✅ Tamamen ücretsiz
- ✅ Tamamen lokal
- ✅ Gizlilik korunur
- ✅ İnternet gerekmez
- ✅ Hızlı çalışır

Başarılar! 🚀

