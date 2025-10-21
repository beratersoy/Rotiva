# 🧭 Rotiva - AI Etkinlik Asistanı

<div align="center">

**Kocaeli ve Sakarya'daki etkinlikleri keşfetmenin en akıllı yolu!**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[🚀 Canlı Demo](https://rotiva-app.streamlit.app) | [📖 Dokümantasyon](#-proje-hakkında) | [🐛 Sorun Bildir](https://github.com/beratersoy/rotivaco/issues)

</div>

---

## 🎯 Proje Hakkında

**Rotiva**, yapay zeka destekli akıllı etkinlik asistanıdır. **Kocaeli ve Sakarya** şehirlerindeki etkinlikleri otomatik olarak toplar, analiz eder ve kullanıcılara kişiselleştirilmiş öneriler sunar.

### 🌟 Öne Çıkan Özellikler

- **🤖 Gemini 2.5 Flash AI**: Google'ın en gelişmiş dil modeli
- **🧠 FAISS Semantic Search**: Facebook AI'ın vektör veritabanı
- **🦜 LangChain Framework**: Enterprise-grade RAG pipeline
- **📊 Sentence-Transformers**: 384-boyutlu multilingual embeddings
- **🔗 Clickable Links**: Her etkinlik için direkt bilet linki
- **📅 Smart Filtering**: Otomatik tarih ve kaynak filtreleme
- **💾 Google Sheets Integration**: Kullanıcı takibi ve analytics

---

## 🏗️ Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────┐
│                   ROTIVA AI ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │ Web Scraping │──────│  JSON Cache  │──────│   FAISS   │ │
│  │   Layer      │      │   Layer      │      │  Vector   │ │
│  │              │      │              │      │    DB     │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│  • Biletinial          • 64 Events           • 384-dim     │
│  • BUBilet             • Auto Refresh        • Embeddings  │
│  • Link Support        • Fast Load           • L2 Distance │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            LANGCHAIN RAG PIPELINE                       │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │ │
│  │  │Retriever │→│  Prompt  │→│  Gemini 2.5 Flash    │ │ │
│  │  │  FAISS   │  │ Template │  │   (Generation)       │ │ │
│  │  └──────────┘  └──────────┘  └──────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            STREAMLIT WEB INTERFACE                      │ │
│  │  • RAG + AI Always Active  • Purple AI Badge           │ │
│  │  • Markdown Link Rendering  • Google Sheets Tracking   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ Teknoloji Stack

### 🔬 Core Technologies

| Kategori | Teknoloji | Versiyon | Kullanım |
|----------|-----------|----------|----------|
| **AI Model** | Google Gemini 2.5 Flash | Latest | Text generation |
| **Embedding** | Sentence-Transformers | 5.1.1 | Semantic embeddings (384-dim) |
| **Vector DB** | FAISS | 1.12.0 | Similarity search |
| **RAG Framework** | LangChain | 0.3.27 | Pipeline orchestration |
| **Web Framework** | Streamlit | 1.28+ | User interface |
| **Scraping** | BeautifulSoup4 | 4.12+ | HTML parsing |
| **ML Library** | Scikit-learn | 1.3+ | TF-IDF fallback |
| **Deep Learning** | PyTorch | 2.9.0 | Embedding backend |

### 📦 Proje Gereksinimleri Karşılaması

✅ **Generation Model**: Google Gemini 2.5 Flash  
✅ **Embedding Model**: Sentence-Transformers (Huggingface - paraphrase-multilingual-MiniLM-L12-v2)  
✅ **Vektor Database**: FAISS (Facebook AI Similarity Search)  
✅ **RAG Framework**: LangChain  

---

## 🚀 Kurulum

### 1️⃣ Repository'yi Klonlayın

```bash
git clone https://github.com/beratersoy/rotiva.git
cd rotiva
```

### 2️⃣ Virtual Environment Oluşturun

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4️⃣ API Key Ayarlayın

```bash
# .env dosyası oluşturun
cp .env.example .env

# .env dosyasını düzenleyin
# GEMINI_API_KEY=your_key_here
```

**Gemini API Key Alma:**
1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. "Create API Key" butonuna tıklayın
3. Key'i kopyalayıp `.env` dosyasına yapıştırın

### 5️⃣ Uygulamayı Çalıştırın

```bash
streamlit run web_app/rotiva_streamlit.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.

---

## 💡 Kullanım

### 🎭 Örnek Sorgular

```
👤 "Kocaeli'de konser var mı?"
🤖 Kocaeli'de 3 konser buldum:
    • [Sagopa Kajmer](https://link) - 15 Kasım
    • [Business Night](https://link) - 23 Ekim
    ...

👤 "Sakarya'da yarın tiyatro var mı?"
🤖 Sakarya'da yarın 2 tiyatro oyunu var:
    • [Mahşer-i Cümbüş](https://link) - 09 Kasım
    • [Cimri](https://link) - 08 Kasım

👤 "16 Ekim'de ne yapabilirim?"
🤖 16 Ekim'de 3 etkinlik var:
    • [Vitray Workshop](https://link) - 550₺
    • [Kaç Zamparalık Gece](https://link) - 750₺
    ...
```

### 🧪 Test Çalıştırma

```bash
# Sistem testlerini çalıştırın
python test_system.py

# Çıktı:
# *** ROTIVA AI - SISTEM TESTI ***
# 1. Cache Kontrolu...
#    OK: 55 etkinlik yuklendi
#    OK: 55/55 etkinlikte link var
# 2. FAISS Retriever Testi...
#    OK: FAISS calisiyor - 3 sonuc bulundu
# 3. RAG Engine Testi...
#    OK: RAG Engine calisiyor
# 4. Gemini API Testi...
#    OK: Gemini API calisiyor
# ==================================================
# BASARILI! TUM TESTLER GECTI!
```

---

## 📊 Veri Kaynakları

### Desteklenen Siteler

| Kaynak | Etkinlik Sayısı | Başarı Oranı | Link Desteği |
|--------|----------------|--------------|--------------|
| 🎫 **Biletinial** | 24 | %80+ | ✅ |
| 🎭 **BUBilet** | 40 | %95+ | ✅ |

**Toplam**: 64 etkinlik (55 aktif - 9 geçmiş tarihli filtrelendi)

---

## 🔬 RAG Pipeline Detayları

### 1. Embedding (Sentence-Transformers)

```python
from sentence_transformers import SentenceTransformer

# Model: paraphrase-multilingual-MiniLM-L12-v2
# - 384 boyutlu vektörler
# - Türkçe optimized
# - ~471MB model boyutu
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Etkinlikleri embedding'e çevir
event_texts = [f"{e['name']} {e['city']}" for e in events]
embeddings = model.encode(event_texts)  # Shape: (55, 384)
```

### 2. FAISS Vector Database

```python
import faiss

# FAISS IndexFlatL2 (L2 distance)
index = faiss.IndexFlatL2(384)
index.add(embeddings)  # 55 etkinlik indekslendi

# Semantic search
query_vector = model.encode(["konser"])
distances, indices = index.search(query_vector, k=5)

# Similarity score: 1 / (1 + L2_distance)
```

### 3. LangChain RAG

```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Gemini 2.5 Flash initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.7,
    google_api_key=api_key
)

# Prompt template with link instructions
template = """
Şu etkinlikler bulundu:
{context}

Kullanıcı sorusu: {query}

Her etkinlik için markdown link formatı kullan:
**[Etkinlik İsmi](link)** — Detaylar
"""

prompt = PromptTemplate(template=template, input_variables=["context", "query"])
chain = LLMChain(llm=llm, prompt=prompt)

# Generate response
response = chain.run(context=context, query=user_query)
```

---

## 📁 Proje Yapısı

```
rotivaco/
├── 📁 data_scraper/              # Web scraping
│   ├── base_scraper.py          # Base scraper class
│   ├── biletinial_scraper.py    # Biletinial scraper (✅ link support)
│   ├── bubilet_scraper.py       # BUBilet scraper (✅ link support)
│   └── event_manager.py         # Data manager (date/source filtering)
│
├── 📁 rag_pipeline/              # RAG system
│   ├── retriever.py             # FAISS retriever (384-dim embeddings)
│   └── rag_engine.py            # LangChain RAG engine
│
├── 📁 utils/                     # Utilities
│   ├── llm_client.py            # Gemini client
│   └── sheets_manager.py        # Google Sheets integration
│
├── 📁 web_app/                   # Streamlit app
│   └── rotiva_streamlit.py      # Main app (always RAG+AI enabled)
│
├── 📁 data/cache/                # JSON cache
│   ├── all_events.json          # All events (64)
│   ├── biletinial_events.json   # Biletinial (24)
│   └── bubilet_events.json      # BUBilet (40)
│
├── 📄 test_system.py             # System tests
├── 📄 requirements.txt           # Dependencies
├── 📄 .env.example               # Environment template
└── 📄 README.md                  # This file
```

---

## ✨ Yeni Özellikler (v1.0.0)

### 🔗 Clickable Links
- Her etkinlik için direkt bilet satış linki
- Markdown formatında (`[Etkinlik](link)`)
- Streamlit otomatik render ediyor

### 📅 Smart Filtering
- **Tarih Filtresi**: Geçmiş etkinlikler otomatik filtreleniyor
- **Kaynak Filtresi**: Sadece Biletinial + BUBilet gösteriliyor
- 64 etkinlik → 55 aktif etkinlik

### 🤖 Always Active RAG+AI
- Kullanıcıya checkbox gösterilmiyor
- Sistem her zaman RAG+AI ile çalışıyor
- Purple "RAG + AI Aktif" badge sidebar'da

### 🧠 Advanced RAG Pipeline
- **FAISS**: L2 distance ile semantic search
- **Sentence-Transformers**: 384-dim multilingual embeddings
- **LangChain**: Enterprise-grade orchestration
- **Gemini 2.5 Flash**: State-of-the-art generation

---

## 📈 Performans

| Metrik | Değer | Notlar |
|--------|-------|--------|
| **Toplam Etkinlik** | 64 | Biletinial (24) + BUBilet (40) |
| **Aktif Etkinlik** | 55 | 9 geçmiş tarihli filtrelendi |
| **Link Coverage** | 100% | Tüm etkinliklerde link var |
| **Embedding Model** | 471MB | İlk yüklemede indirilir |
| **FAISS Indexing** | ~50ms | 55 etkinlik için |
| **RAG Response** | ~1.5s | Embedding + FAISS + Gemini |
| **Cache Hit** | <0.5s | JSON cache kullanımında |

---

## 🔮 Gelecek Planları

### Kısa Vadeli
- [ ] Biletix scraper iyileştirmesi
- [ ] Daha fazla şehir desteği
- [ ] Kategori filtreleme (müzik, tiyatro, spor)
- [ ] Fiyat aralığı filtresi

### Orta Vadeli
- [ ] Vector DB migration (Pinecone/Weaviate)
- [ ] Fine-tuned embedding model
- [ ] User preference learning
- [ ] Email notifications

### Uzun Vadeli
- [ ] Mobil uygulama (React Native)
- [ ] Çoklu dil desteği
- [ ] Sosyal özellikler (paylaşım, yorum)
- [ ] Public REST API

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermeden önce:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit yapın (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır.

---

## 📞 İletişim

**Proje Sahibi**: Berat Ersoy

- GitHub: [@beratersoy](https://github.com/beratersoy)
- Email: portberat@gmail.com
- LinkedIn: [beratersoy](https://linkedin.com/in/beratersoy)

---

## 🙏 Teşekkürler

- **Google AI** - Gemini 2.5 Flash API
- **Facebook AI** - FAISS vector database
- **Hugging Face** - Sentence-Transformers
- **LangChain** - RAG framework
- **Streamlit** - Web framework
- **Python Community** - Mükemmel ekosistem
- **Data** -- Biletinial - Bubilet
---

<div align="center">

### 🧭 Rotiva ile etkinliklerinizi keşfedin!

**[🚀 Canlı Demo'yu Deneyin](https://rotiva-app.streamlit.app)**

*"AI etkinlik keşfi için en akıllı çözüm"*

**Made with ❤️ and 🤖 by [Berat Ersoy](https://github.com/beratersoy)**

⭐ **Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

</div>
