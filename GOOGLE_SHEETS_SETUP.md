# Google Sheets Entegrasyonu Kurulum Rehberi

## 🎯 Amaç
Kullanıcıların isim ve e-posta bilgilerini Google Sheets'e otomatik kaydetmek.

## 📋 Adımlar

### 1. Google Cloud Console'da Proje Oluştur
1. [Google Cloud Console](https://console.cloud.google.com/) adresine git
2. Yeni proje oluştur: **"Rotiva Event Manager"**
3. Projeyi seç

### 2. Google Sheets API'yi Aktifleştir
1. Sol menüden **"APIs & Services" > "Library"**
2. **"Google Sheets API"** ara ve aktifleştir
3. **"Google Drive API"** ara ve aktifleştir

### 3. Service Account Oluştur
1. **"APIs & Services" > "Credentials"**
2. **"Create Credentials" > "Service Account"**
3. İsim: `rotiva-sheets-manager`
4. Role: **Editor**
5. **"Create and Continue"** tıkla
6. **"Done"** tıkla

### 4. JSON Key Oluştur
1. Oluşturduğun Service Account'a tıkla
2. **"Keys"** sekmesine git
3. **"Add Key" > "Create New Key"**
4. **JSON** formatını seç
5. İndirilecek dosyayı **`credentials.json`** olarak kaydet
6. Bu dosyayı proje klasörüne (`rotivaco/`) taşı

### 5. Google Sheets Oluştur
1. [Google Sheets](https://sheets.google.com/) adresine git
2. Yeni sayfa oluştur
3. İsim: **"Rotiva Kullanıcılar"**
4. **Service Account e-postasını** sheet'e paylaş (Editor yetkisi ile)
   - `credentials.json` içindeki `client_email` değerini kopyala
   - Örnek: `rotiva-sheets-manager@rotiva-event-manager.iam.gserviceaccount.com`
   - Sheet'te **Share** butonuna tıkla
   - Bu e-postayı ekle ve **Editor** yetkisi ver

### 6. Test Et
```bash
cd C:\Users\hp\Desktop\rotivaco
venv\Scripts\python.exe utils\sheets_manager.py
```

Çıktı:
```
✅ Google Sheets bağlantısı başarılı!
✅ Google Sheets başlıkları oluşturuldu
Toplam kullanıcı: 0
```

## 📊 Google Sheets Yapısı

| Tarih | İsim Soyisim | E-posta | İşlem |
|-------|--------------|---------|-------|
| 2025-10-17 14:30:00 | Ahmet Yılmaz | ahmet@example.com | Kayıt |
| 2025-10-17 14:35:00 | - | - | Atla |

## ✅ Entegrasyon Durumu

- ✅ `gspread` ve `oauth2client` kütüphaneleri kuruldu
- ✅ `utils/sheets_manager.py` oluşturuldu
- ✅ Streamlit'e entegre edildi
- ✅ `.env` dosyasına config eklendi
- ⏳ Google Cloud Console'da setup yapılacak
- ⏳ `credentials.json` dosyası eklenecek

## 🔒 Güvenlik
- `credentials.json` dosyası `.gitignore`'a eklenmelidir
- Service Account sadece bir sheet'e erişebilir
- API anahtarları asla commit edilmemelidir

## 🚀 Kullanım
Kullanıcılar form doldurduğunda:
1. İsim + Mail + "Başla" → Google Sheets'e tam bilgi kaydedilir
2. "Atla" → Anonim kullanıcı olarak kaydedilir

## 📞 Destek
Sorun yaşarsan:
- Service Account email'i kontrol et
- Sheet'in doğru paylaşıldığından emin ol
- `credentials.json` dosya yolunu kontrol et
