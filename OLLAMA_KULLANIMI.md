#  Ollama ile Lokal Model Kullanımı

Bu kılavuz, projeyi Ollama ile lokal modeller kullanarak çalıştırmanızı sağlar.

##  Avantajlar

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

##  Adım 2: Model İndirme

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

##  Adım 3: Proje Konfigürasyonu

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

##  Adım 4: Projeyi Çalıştırın

```powershell
# Test edin
python main.py test

# Çalıştırın
python main.py
```

##  Model Değiştirme

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

##  Gemini kullanımı

Ollama yerine  Gemini kullanmak isterseniz:

```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_api_key_here
```


