# 🚀 Rotiva Deployment Guide

## Adım 1: GitHub'a Push (ÖNCELİKLE BU!)

### A. Git Kurulumu (İlk Sefer İçin)

**Windows:**
1. https://git-scm.com/download/win adresine gidin
2. Git'i indirip yükleyin
3. PowerShell'i yeniden başlatın

### B. Git Yapılandırması

```bash
# Kullanıcı bilgilerinizi ayarlayın
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### C. Repository Oluşturma

**GitHub'da:**
1. https://github.com adresine gidin
2. "New repository" butonuna tıklayın
3. Repository adı: `rotivaco` (veya istediğiniz)
4. Public veya Private seçin
5. **ÖNEMLİ:** README, .gitignore, license EKLEMEYİN (zaten var)
6. "Create repository" butonuna tıklayın

### D. Lokal Push İşlemi

```bash
# 1. Git repository başlatın
git init

# 2. Tüm dosyaları ekleyin (.gitignore otomatik filtreleyecek)
git add .

# 3. İlk commit
git commit -m "feat: Complete FAISS+LangChain+Gemini RAG system with smart filtering and links"

# 4. Branch adını main yapın (opsiyonel ama önerilen)
git branch -M main

# 5. GitHub repo'nuzu bağlayın (URL'i GitHub'dan kopyalayın)
git remote add origin https://github.com/YOUR_USERNAME/rotivaco.git

# 6. Push edin!
git push -u origin main
```

### E. Güvenlik Kontrolü

Push SONRASINDA GitHub'da kontrol edin:
- ❌ `.env` dosyası OLMAMALI
- ❌ `credentials.json` dosyası OLMAMALI
- ✅ `.gitignore` dosyası OLMALI
- ✅ `.env.example` dosyası OLMALI

**Eğer yanlışlıkla .env push ettiyseniz:**
```bash
# HEMEN ŞİFRELERİ DEĞİŞTİRİN!
# Sonra dosyayı kaldırın:
git rm --cached .env
git commit -m "fix: Remove sensitive .env file"
git push
```

---

## Adım 2: Streamlit Cloud Deploy (GITHUB'DAN SONRA!)

### A. Streamlit Cloud'a Giriş

1. https://streamlit.io/cloud adresine gidin
2. "Sign up" veya "Sign in" yapın
3. GitHub hesabınızla bağlanın (authorize edin)

### B. Yeni App Oluşturma

1. "New app" butonuna tıklayın
2. Formu doldurun:
   - **Repository:** `YOUR_USERNAME/rotivaco`
   - **Branch:** `main`
   - **Main file path:** `web_app/rotiva_streamlit.py`
   - **App URL:** `rotiva-app` (veya istediğiniz)

### C. Secrets Ekleme

**ÖNEMLİ:** Deploy butonuna basmadan ÖNCE!

1. "Advanced settings" açın
2. "Secrets" bölümüne gidin
3. TOML formatında ekleyin:

```toml
GEMINI_API_KEY = "AIzaSyBKe8kUhQIV6kOYZxtW6Bfc9KVoUVIdAsc"

# Google Sheets için (opsiyonel)
# credentials.json içeriğini JSON olarak yapıştırın
```

**credentials.json için:**
```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
```

### D. Deploy!

1. "Deploy!" butonuna tıklayın
2. Deploy sürecini izleyin (3-5 dakika)
3. Logları kontrol edin:
   - ✅ "Installing dependencies"
   - ✅ "Downloading embedding model" (~471MB)
   - ✅ "Your app is live!"

### E. Test Edin

1. App URL'inizi ziyaret edin: `https://rotiva-app.streamlit.app`
2. Test sorguları:
   - "Kocaeli'de konser var mı?"
   - "Sakarya'da tiyatro var mı?"
3. Linklere tıklayın, çalışıyor mu?
4. AI badge'i görünüyor mu?

---

## Adım 3: Sürekli Deployment (Otomatik!)

### Artık Her Push Otomatik Deploy Olur

```bash
# Kod değişikliği yaptınız
git add .
git commit -m "fix: Update something"
git push

# Streamlit Cloud otomatik deploy edecek!
# ~2-3 dakika sonra değişiklikler yayında olacak
```

### Deployment Durumunu İzleme

1. Streamlit Cloud dashboard'a gidin
2. App'inizi seçin
3. "Manage app" → "Logs"
4. Real-time deployment loglarını görün

---

## Adım 4: Domain Ayarları (Opsiyonel)

### Custom Domain Ekleme

1. Streamlit Cloud dashboard
2. App settings → "Custom subdomain"
3. Örnek: `rotiva.streamlit.app` yerine `rotiva-events.streamlit.app`

---

## Troubleshooting

### ❌ "ModuleNotFoundError"
**Çözüm:** `requirements.txt` eksik bağımlılık var
```bash
# Lokal test edin
pip install -r requirements.txt
python -c "from rag_pipeline.rag_engine import RAGEngine"

# Düzelttikten sonra:
git add requirements.txt
git commit -m "fix: Add missing dependency"
git push
```

### ❌ "API Key not found"
**Çözüm:** Streamlit secrets yanlış
1. App settings → Secrets
2. TOML formatını kontrol edin
3. `GEMINI_API_KEY` doğru yazılmış mı?

### ❌ "Embedding model download failed"
**Çözüm:** Timeout problemi
1. Streamlit Cloud bazen ilk seferde timeout verebilir
2. "Reboot app" butonuna basın
3. Model cache'lenecek, sonraki sefer hızlı olacak

### ❌ "Google Sheets connection failed"
**Çözüm:** credentials.json eksik veya hatalı
1. Secrets'ta `gcp_service_account` bölümünü kontrol edin
2. JSON formatı doğru mu?
3. Service account email Google Sheets'e eklendi mi?

---

## Checklist

### ✅ GitHub Push Öncesi
- [ ] `.gitignore` güncel
- [ ] `.env` ignore ediliyor
- [ ] `credentials.json` ignore ediliyor
- [ ] `requirements.txt` tüm bağımlılıkları içeriyor
- [ ] README.md güncel

### ✅ Streamlit Deploy Öncesi
- [ ] GitHub repo public veya Streamlit'e erişim verildi
- [ ] `web_app/rotiva_streamlit.py` doğru path
- [ ] Secrets eklendi (GEMINI_API_KEY)
- [ ] Optional: Google Sheets credentials eklendi

### ✅ Deploy Sonrası
- [ ] App başarıyla yüklendi
- [ ] AI badge görünüyor
- [ ] Test sorguları çalışıyor
- [ ] Linkler tıklanabiliyor
- [ ] Google Sheets'e kayıt oluyor (varsa)

---

## Hızlı Komutlar

```bash
# GitHub push
git add .
git commit -m "your message"
git push

# Streamlit reboot (problem varsa)
# Dashboard → Manage app → Reboot app

# Logs görüntüleme
# Dashboard → Manage app → Logs
```

---

## İletişim & Destek

**Sorun mu var?**
- GitHub Issues: https://github.com/YOUR_USERNAME/rotivaco/issues
- Streamlit Community: https://discuss.streamlit.io/

**Başarılar! 🚀**
