import json
import time
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class BaseEventScraper:
    """Tüm scraperların türediği temel sınıf - Anti-bot koruması ve ortak fonksiyonlar"""
    
    # Modern tarayıcı başlıkları - Bot algılamayı bypass etmek için
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr,en-US;q=0.9,en;q=0.8,de;q=0.7,fr;q=0.6,ca;q=0.5,id;q=0.4,pt-BR;q=0.3,pt;q=0.2,ms;q=0.1,no;q=0.1,ar;q=0.1,pl;q=0.1,es;q=0.1',       
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        
    }
    
    def __init__(self):
        self.cache_dir = Path("./data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.min_delay = 1
        self.max_delay = 5
    
    def wait_random(self, label=""):
        """Rastgele süre bekle (1-5 saniye arası) - İnsan davranışını taklit etmek için"""
        delay = random.uniform(self.min_delay, self.max_delay)
        if label:
            print(f"⏳ {label} ({delay:.1f}s)")
        time.sleep(delay)
    
    def setup_driver(self):
        """Selenium Chrome driver'ı oluştur - Gelişmiş anti-bot ayarları ile"""
        options = Options()
        
        # Bot algılamayı engellemek için gerekli ayarlar
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        import tempfile
        temp_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={temp_dir}")
        options.add_argument("--remote-debugging-port=9222")
        
        # User-Agent seçimi: Varsayılan mobil UA. Scraper'da use_desktop=True ise masaüstü UA kullan
        mobile_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        desktop_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        ua = desktop_user_agent if getattr(self, 'use_desktop', False) else mobile_user_agent
        options.add_argument(f"user-agent={ua}")
        
        # Pencere boyutu - iPhone ekran ölçüleri
        options.add_argument("--window-size=375,812")
        
        # Webdriver'ı gizle - Bot algılamasını engelle
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Chrome DevTools Protocol komutları - Webdriver izlerini sil
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['tr-TR', 'tr', 'en-US', 'en']});
                window.chrome = {runtime: {}};
            """
        })
        
        print("✅ Driver hazır (gelişmiş anti-bot koruması aktif)")
        return driver
    
    def clean_text(self, text):
        """Metindeki fazla boşlukları temizle ve tek satıra indir"""
        return ' '.join(text.split())
    
    # --- Tarih İşleme Fonksiyonları ---
    def parse_date_from_text(self, text: str):
        """Türkçe metinden YYYY-MM-DD formatında tarih çıkar. Bulamazsa None döner.
        Örnekler: '23 Ekim', '23 Ekim Per - 20:00', '02 Kasım Paz - 21:00'
        Not: Yıl belirtilmemişse mevcut yılı varsayar.
        """
        if not text:
            return None
        import re
        from datetime import datetime
        t = text.lower()
        # Türkçe ay isimleri ve karşılık gelen sayıları
        month_to_num = {
            'ocak': 1, 'şubat': 2, 'subat': 2, 'mart': 3, 'nisan': 4, 'mayıs': 5, 'mayis': 5,
            'haziran': 6, 'temmuz': 7, 'ağustos': 8, 'agustos': 8, 'eylül': 9, 'eylul': 9,
            'ekim': 10, 'kasım': 11, 'kasim': 11, 'aralık': 12, 'aralik': 12,
        }
        # Gün + Ay formatını bul (örnek: "23 ekim")
        m = re.search(r"\b(\d{1,2})\s+(ocak|şubat|subat|mart|nisan|mayıs|mayis|haziran|temmuz|ağustos|agustos|eylül|eylul|ekim|kasım|kasim|aralık|aralik)\b", t)
        if not m:
            return None
        try:
            day = int(m.group(1))
            month = month_to_num.get(m.group(2))
            if not month:
                return None
            year = datetime.now().year
            dt = datetime(year, month, day)
            return dt.strftime('%Y-%m-%d')
        except Exception:
            return None
    
    @staticmethod
    def normalize_event_date(event_date_str):
        """
        Etkinlik tarihini ISO formatına (YYYY-MM-DD) çevir.
        Giriş örnekleri: "23 Ekim 2025", "23 Ekim", "23 Ekim Per - 20:00"
        Çıkış: "2025-10-23" veya None (başarısızsa)
        """
        if not event_date_str:
            return None
        
        import re
        from datetime import datetime
        
        text = event_date_str.lower().strip()
        
        month_to_num = {
            'ocak': 1, 'şubat': 2, 'subat': 2, 'mart': 3, 'nisan': 4, 
            'mayıs': 5, 'mayis': 5, 'haziran': 6, 'temmuz': 7, 
            'ağustos': 8, 'agustos': 8, 'eylül': 9, 'eylul': 9,
            'ekim': 10, 'kasım': 11, 'kasim': 11, 'aralık': 12, 'aralik': 12,
        }
        
        # Gün + Ay + (opsiyonel Yıl) formatını ara
        pattern = r"(\d{1,2})\s+(ocak|şubat|subat|mart|nisan|mayıs|mayis|haziran|temmuz|ağustos|agustos|eylül|eylul|ekim|kasım|kasim|aralık|aralik)(?:\s+(\d{4}))?"
        match = re.search(pattern, text)
        
        if match:
            try:
                day = int(match.group(1))
                month = month_to_num.get(match.group(2))
                year = int(match.group(3)) if match.group(3) else datetime.now().year
                
                if month and 1 <= day <= 31:
                    dt = datetime(year, month, day)
                    return dt.strftime('%Y-%m-%d')
            except ValueError:
                pass
        
        return None
    
    @staticmethod
    def parse_turkish_date_query(query_text):
        """
        Kullanıcının Türkçe sorgusundan tarih aralığı çıkar.
        Örnekler:
        - "19 ekim" -> ("2025-10-19", "2025-10-19")
        - "bu hafta sonu" -> (cumartesi, pazar tarihleri)
        - "önümüzdeki 7 gün" -> (bugün, 7 gün sonrası)
        - "kasım ayı" -> ("2025-11-01", "2025-11-30")
        
        Returns: (başlangıç_tarihi, bitiş_tarihi) tuple (ISO format) veya (None, None)
        """
        import re
        from datetime import datetime, timedelta
        
        text = query_text.lower().strip()
        today = datetime.now()
        
        month_to_num = {
            'ocak': 1, 'şubat': 2, 'subat': 2, 'mart': 3, 'nisan': 4,
            'mayıs': 5, 'mayis': 5, 'haziran': 6, 'temmuz': 7,
            'ağustos': 8, 'agustos': 8, 'eylül': 9, 'eylul': 9,
            'ekim': 10, 'kasım': 11, 'kasim': 11, 'aralık': 12, 'aralik': 12,
        }
        
        # 1. Belirli gün formatı: "19 ekim"
        pattern = r"(\d{1,2})\s+(ocak|şubat|subat|mart|nisan|mayıs|mayis|haziran|temmuz|ağustos|agustos|eylül|eylul|ekim|kasım|kasim|aralık|aralik)"
        match = re.search(pattern, text)
        if match:
            try:
                day = int(match.group(1))
                month = month_to_num.get(match.group(2))
                if month and 1 <= day <= 31:
                    year = today.year
                    dt = datetime(year, month, day)
                    # Geçmiş tarihse bir sonraki yıla al
                    if dt < today:
                        dt = datetime(year + 1, month, day)
                    date_str = dt.strftime('%Y-%m-%d')
                    return (date_str, date_str)
            except ValueError:
                pass
        
        # 2. Ay bazlı sorgular: "kasım ayı", "kasımda"
        for month_name, month_num in month_to_num.items():
            if month_name in text:
                year = today.year
                if month_num < today.month:
                    year += 1  # Geçmiş ay ise gelecek yıl olarak al
                start = datetime(year, month_num, 1)
                # Ayın son gününü hesapla
                if month_num == 12:
                    end = datetime(year, 12, 31)
                else:
                    end = datetime(year, month_num + 1, 1) - timedelta(days=1)
                return (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        
        # 3. Hafta sonu sorguları: "bu hafta sonu", "haftasonu"
        if 'bu hafta sonu' in text or 'haftasonu' in text:
            # Cumartesi gününe kadar olan gün sayısını hesapla
            days_until_saturday = (5 - today.weekday()) % 7
            saturday = today + timedelta(days=days_until_saturday)
            sunday = saturday + timedelta(days=1)
            return (saturday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d'))
        
        # 4. Günlük ve haftalık sorgular: "bugün", "yarın", "bu hafta"
        if 'bugün' in text or 'bugun' in text:
            return (today.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
        
        if 'yarın' in text or 'yarin' in text:
            tomorrow = today + timedelta(days=1)
            return (tomorrow.strftime('%Y-%m-%d'), tomorrow.strftime('%Y-%m-%d'))
        
        if 'bu hafta' in text:
            end_of_week = today + timedelta(days=(6 - today.weekday()))
            return (today.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d'))
        
        # 5. Gün sayısı bazlı: "önümüzdeki X gün", "gelecek 7 gün"
        match = re.search(r'(?:önümüzdeki|onumdeki)\s+(\d+)\s+gün', text)
        if match:
            days = int(match.group(1))
            end_date = today + timedelta(days=days)
            return (today.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        return (None, None)
    
    def get_cache(self, cache_file):
        """Cache'den yükle"""
        cache_path = Path(cache_file)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"📂 Cache yüklendi: {len(data)} etkinlik")
                return data
            except:
                return None
        return None
    
    def save_cache(self, data, cache_file):
        """Cache'e kaydet"""
        try:
            cache_path = Path(cache_file)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 Cache kaydedildi: {len(data)} etkinlik")
        except Exception as e:
            print(f"❌ Cache hatası: {e}")
    
    def is_target_city(self, event_data):
        """Kocaeli veya Sakarya mı kontrol et"""
        location = event_data.get('location', '').lower()
        city = event_data.get('city', '').lower()
        title = event_data.get('title', '').lower()
        url = event_data.get('url', '').lower()
        source = event_data.get('source', '').lower()
        
        # Tüm alanları birleştir
        combined = f"{location} {city} {title} {url} {source}".lower()
        
        kocaeli_words = ['kocaeli', 'izmit']
        sakarya_words = ['sakarya', 'adapazarı']
        
        # URL'de şehir adı varsa kabul et
        if '/kocaeli/' in url or '/sakarya/' in url:
            return True
            
        # Diğer alanlarda şehir adı varsa kabul et
        for word in kocaeli_words + sakarya_words:
            if word in combined:
                return True
        return False

    def ensure_city(self, event_data, url_key: str = ''):
        """Eğer event_data['city'] boşsa url_key veya url üzerinden şehir tahmini yapıp doldurur."""
        if event_data.get('city'):
            return event_data
        # url_key bazlı atama
        if url_key:
            lk = url_key.lower()
            if 'kocaeli' in lk:
                event_data['city'] = 'Kocaeli'
                return event_data
            if 'sakarya' in lk:
                event_data['city'] = 'Sakarya'
        # url üzerinden kontrol
        url = (event_data.get('url') or '').lower()
        if '/kocaeli/' in url:
            event_data['city'] = 'Kocaeli'
        elif '/sakarya/' in url:
            event_data['city'] = 'Sakarya'
        return event_data