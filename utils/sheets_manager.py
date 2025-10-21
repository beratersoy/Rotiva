"""
Google Sheets Manager - Kullanıcı verilerini Google Sheets'e kaydetme
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class SheetsManager:
    def __init__(self):
        """Google Sheets bağlantısını başlat ve ayarları yükle"""
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'Rotiva Kullanıcılar')
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID', None)  # Sheet ID ile doğrudan açmak için
        self.client = None
        self.sheet = None
        
    def connect(self):
        """Google Sheets API'ye bağlan ve sayfayı aç"""
        try:
            if not os.path.exists(self.credentials_file):
                print(f"⚠️ Credentials dosyası bulunamadı: {self.credentials_file}")
                return False
                
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, 
                self.scope
            )
            self.client = gspread.authorize(creds)
            
            # Sheet ID varsa onunla aç (daha hızlı), yoksa isimle ara
            if self.sheet_id:
                self.sheet = self.client.open_by_key(self.sheet_id).sheet1
            else:
                self.sheet = self.client.open(self.sheet_name).sheet1
            
            print("✅ Google Sheets bağlantısı başarılı!")
            return True
        except Exception as e:
            import traceback
            print(f"❌ Google Sheets bağlantı hatası: {type(e).__name__}: {e}")
            print(f"Detay: {traceback.format_exc()}")
            return False
    
    def save_user(self, name: str, email: str, skip: bool = False):
        """
        Kullanıcı bilgilerini Google Sheets'e kaydet
        
        Args:
            name: Kullanıcı adı soyadı
            email: E-posta adresi
            skip: Hızlı başla butonu kullanıldı mı?
        """
        if not self.sheet:
            if not self.connect():
                print("⚠️ Google Sheets bağlantısı kurulamadı, veri kaydedilemiyor")
                return False
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            action = "Atla" if skip else "Kayıt"
            
            # Yeni satır ekle (tarih, isim, email, işlem)
            row = [timestamp, name if name else "-", email if email else "-", action]
            self.sheet.append_row(row)
            
            print(f"✅ Kullanıcı kaydedildi: {name or 'Anonim'}")
            return True
        except Exception as e:
            print(f"❌ Kullanıcı kaydetme hatası: {e}")
            return False
    
    def initialize_sheet(self):
        """Başlık satırını oluştur (ilk kurulumda)"""
        if not self.sheet:
            if not self.connect():
                return False
        
        try:
            # İlk satırda başlık satırı var mı kontrol et
            first_row = self.sheet.row_values(1)
            if not first_row or first_row[0] != "Tarih":
                # Başlık satırı ekle
                headers = ["Tarih", "İsim Soyisim", "E-posta", "İşlem"]
                self.sheet.insert_row(headers, 1)
                print("✅ Google Sheets başlıkları oluşturuldu")
            return True
        except Exception as e:
            print(f"❌ Başlık oluşturma hatası: {e}")
            return False
    
    def get_user_count(self):
        """Toplam kullanıcı sayısını getir"""
        if not self.sheet:
            if not self.connect():
                return 0
        
        try:
            # İlk satır başlık satırı, geri kalan satırlar kullanıcı verisi
            return len(self.sheet.get_all_records())
        except Exception as e:
            print(f"❌ Kullanıcı sayısı okuma hatası: {e}")
            return 0


# Modülü doğrudan çalıştırarak test etmek için
if __name__ == "__main__":
    manager = SheetsManager()
    if manager.connect():
        manager.initialize_sheet()
        print(f"Toplam kullanıcı: {manager.get_user_count()}")
