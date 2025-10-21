# 📊 Google Sheets API - Detaylı Kurulum Rehberi

## 🎯 Ne Yapacağız?
Kullanıcı bilgilerini otomatik olarak Google Sheets'e kaydetmek için API bağlantısı kuracağız.

---

## 📝 ADIM 1: Google Cloud Console'a Giriş

1. **Tarayıcıda aç:** https://console.cloud.google.com/
2. Google hesabınla giriş yap (Gmail hesabın)
3. Üst kısımda **"Select a project"** (Proje seç) tıkla
4. **"NEW PROJECT"** (Yeni Proje) butonuna tıkla

---

## 📝 ADIM 2: Yeni Proje Oluştur

1. **Project name:** `Rotiva-Event-Manager` yaz
2. **Location:** "No organization" olarak bırak
3. **CREATE** butonuna tıkla
4. 5-10 saniye bekle, proje oluşacak
5. Bildirim gelince **"SELECT PROJECT"** tıkla

---

## 📝 ADIM 3: Google Sheets API'yi Aktifleştir

### 3.1 - Kütüphaneyi Aç
1. Sol üst köşede **☰** (hamburger menu) tıkla
2. **"APIs & Services"** üzerine gel
3. **"Library"** (Kütüphane) tıkla

### 3.2 - Google Sheets API
1. Arama kutusuna **"Google Sheets API"** yaz
2. İlk sonuca tıkla
3. Mavi **"ENABLE"** (Etkinleştir) butonuna tıkla
4. Sayfa yüklenince üstte "API enabled" yazacak

### 3.3 - Google Drive API (aynı işlem)
1. Tekrar **☰ > APIs & Services > Library**
2. Arama kutusuna **"Google Drive API"** yaz
3. İlk sonuca tıkla
4. Mavi **"ENABLE"** butonuna tıkla

---

## 📝 ADIM 4: Service Account Oluştur (ÖNEMLİ!)

### 4.1 - Credentials Sayfasına Git
1. Sol menüden **"Credentials"** (Kimlik Bilgileri) tıkla
2. Üstte **"+ CREATE CREDENTIALS"** tıkla
3. Açılan menüden **"Service account"** seç

### 4.2 - Service Account Detayları
**İlk Sayfa:**
- **Service account name:** `rotiva-sheets-manager` yaz
- **Service account ID:** Otomatik doldurulacak
- **Description:** `Kullanıcı verilerini Google Sheets'e kaydetmek için` yaz
- **CREATE AND CONTINUE** tıkla

**İkinci Sayfa (Grant Access):**
- **Select a role** dropdown'ına tıkla
- Arama kutusuna **"Editor"** yaz
- **Editor** seç
- **CONTINUE** tıkla

**Üçüncü Sayfa:**
- Boş bırak, **DONE** tıkla

---

## 📝 ADIM 5: JSON Key Dosyası İndir (KRİTİK!)

### 5.1 - Keys Oluştur
1. Az önce oluşturduğun Service Account'u göreceksin
2. **E-posta adresi** var mı kontrol et (örnek: `rotiva-sheets-manager@rotiva-event-manager.iam.gserviceaccount.com`)
3. Bu **E-POSTA ADRESİNİ KOPYALA** (sonra lazım olacak)
4. Service account'a **tıkla** (satırın üzerine)

### 5.2 - JSON Key İndir
1. Üstteki sekmelerden **"KEYS"** tıkla
2. **"ADD KEY"** dropdown tıkla
3. **"Create new key"** seç
4. **JSON** seçili olacak, **CREATE** tıkla
5. Otomatik olarak bir `.json` dosyası indirilecek
6. Bu dosyanın adı: `rotiva-event-manager-xxxxx.json` gibi bir şey olacak

### 5.3 - Dosyayı Taşı
1. İndirilen JSON dosyasını bul (muhtemelen Downloads klasöründe)
2. Dosyayı **kopyala**
3. Proje klasörüne yapıştır: `C:\Users\hp\Desktop\rotivaco\`
4. Dosya ismini değiştir: **`credentials.json`** olarak kaydet

---

## 📝 ADIM 6: Google Sheets Oluştur

### 6.1 - Yeni Sheet Oluştur
1. **Yeni sekmede aç:** https://sheets.google.com/
2. Yeşil **"+"** butonuna tıkla (Blank spreadsheet)
3. Üstte **"Untitled spreadsheet"** yazan yere tıkla
4. İsim gir: **`Rotiva Kullanıcılar`** (tam olarak böyle yaz)
5. Enter'a bas

### 6.2 - Service Account'u Paylaş (ÇOK ÖNEMLİ!)
1. Sağ üstteki **"Share"** (Paylaş) butonuna tıkla
2. **ADIM 5.1'de kopyaladığın e-posta adresini yapıştır**
   - Örnek: `rotiva-sheets-manager@rotiva-event-manager.iam.gserviceaccount.com`
3. Sağ tarafta **"Editor"** (Düzenleyici) seçili olsun
4. **"Notify people"** (İnsanları bilgilendir) kutusunun **işaretini kaldır**
5. **"Share"** veya **"Send"** tıkla
6. ✅ "Shared with 1 person" gibi bir mesaj göreceksin

---

## 📝 ADIM 7: Test Et!

### 7.1 - Terminal Komutları
```powershell
cd C:\Users\hp\Desktop\rotivaco
venv\Scripts\python.exe utils\sheets_manager.py
```

### 7.2 - Beklenen Çıktı
```
✅ Google Sheets bağlantısı başarılı!
✅ Google Sheets başlıkları oluşturuldu
Toplam kullanıcı: 0
```

### 7.3 - Google Sheets'i Kontrol Et
1. Tarayıcıda açık olan "Rotiva Kullanıcılar" sheet'ine git
2. İlk satırda başlıklar göreceksin:

| Tarih | İsim Soyisim | E-posta | İşlem |
|-------|--------------|---------|-------|
|       |              |         |       |

---

## ❌ Sık Karşılaşılan Hatalar

### Hata 1: "File not found: credentials.json"
**Çözüm:** 
- JSON dosyasını doğru klasöre koyduğundan emin ol
- Dosya adı tam olarak `credentials.json` olmalı

### Hata 2: "Spreadsheet not found"
**Çözüm:**
- Google Sheets isminin **tam olarak** "Rotiva Kullanıcılar" olduğundan emin ol
- `.env` dosyasındaki `GOOGLE_SHEET_NAME` değerini kontrol et

### Hata 3: "Permission denied"
**Çözüm:**
- Service Account e-postasını sheet'e paylaştığından emin ol
- Editor yetkisi verdiğinden emin ol
- E-posta adresini doğru kopyaladığını kontrol et

### Hata 4: "API not enabled"
**Çözüm:**
- Google Sheets API ve Google Drive API'nin aktif olduğunu kontrol et
- Cloud Console'da **APIs & Services > Dashboard** sayfasından kontrol et

---

## 🎉 Başarılı Kurulum Sonrası

Artık Streamlit uygulamasında kullanıcılar kayıt olduğunda:
- ✅ Bilgiler otomatik olarak Google Sheets'e kaydedilecek
- ✅ Tarih-saat damgası eklenecek
- ✅ "Atla" veya "Başla" seçimine göre farklı kayıt yapılacak

---

## 📞 Yardıma İhtiyacın Olursa

Hangi adımda takıldığını söyle, o adımı daha detaylı açıklayayım!

**Örnek sorular:**
- "ADIM 3'te kaldım, Library sayfasını bulamıyorum"
- "Service Account oluşturdum ama JSON dosyası indirmiyor"
- "Sheet'i paylaştım ama test ederken hata veriyor"
