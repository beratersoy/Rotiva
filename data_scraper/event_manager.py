"""
Event Manager - Tüm scraper'ları yönetir ve etkinlik verilerini birleştirir
"""

import json
from pathlib import Path
from datetime import datetime
from data_scraper.biletinial_scraper import BiletinialScraper
from data_scraper.bubilet_scraper import BUBiletScraper


class EventManager:
    """Etkinlik yöneticisi - Tüm kaynaklardan veri toplama ve önbellekleme"""
    
    # Scraping yapılan resmi kaynaklar (sadece bunlar gösterilecek)
    ALLOWED_SOURCES = ['Biletinial', 'BUBilet']
    
    def __init__(self, use_cache=True):
        self.cache_dir = Path("./data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.combined_cache_file = self.cache_dir / "all_events.json"
        self.events = []
        self.use_cache = use_cache
        
        self.load_or_scrape()
    
    def load_or_scrape(self):
        """Önbellekten yükle veya yeni veri topla (scrape)"""
        
        if self.use_cache and self.combined_cache_file.exists():
            self.load_from_cache()
        else:
            self.scrape_all()
            self.save_to_cache()
    
    def scrape_all(self):
        """Tüm scraper'ları çalıştır ve etkinlikleri topla (Biletix hariç - çünkü çok yavaş)"""
        print("\n" + "="*60)
        print("🔄 TÜM ETKINLIKLER ÇEKİLİYOR")
        print("="*60 + "\n")
        all_events = []
        # Biletinial sitesinden çek
        print("1️⃣  BİLETİNİAL")
        print("-" * 60)
        try:
            biletinial_scraper = BiletinialScraper()
            biletinial_events = biletinial_scraper.scrape_events()
            all_events.extend(biletinial_events)
            print(f"✅ Biletinial: {len(biletinial_events)} etkinlik\n")
        except Exception as e:
            print(f"❌ Biletinial hatası: {e}\n")
        # BUBilet sitesinden çek
        print("2️⃣  BUBILET")
        print("-" * 60)
        try:
            bubilet_scraper = BUBiletScraper()
            bubilet_events = bubilet_scraper.scrape_events()
            all_events.extend(bubilet_events)
            print(f"✅ BUBilet: {len(bubilet_events)} etkinlik\n")
        except Exception as e:
            print(f"❌ BUBilet hatası: {e}\n")
        print("="*60)
        print(f"✅ TOPLAM: {len(all_events)} ETKİNLİK ÇEKİLDİ")
        print("="*60 + "\n")
        self.events = all_events
    
    def save_to_cache(self):
        """Etkinlik verilerini önbellek dosyasına kaydet (JSON formatında)"""
        try:
            with open(self.combined_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, ensure_ascii=False, indent=2)
            print(f"💾 Önbellek kaydedildi: {len(self.events)} etkinlik\n")
        except Exception as e:
            print(f"❌ Önbellek kaydetme hatası: {e}")
    
    def load_from_cache(self):
        """Önbellekteki etkinlik verilerini yükle"""
        try:
            with open(self.combined_cache_file, 'r', encoding='utf-8') as f:
                self.events = json.load(f)
            print(f"📂 Önbellek yüklendi: {len(self.events)} etkinlik\n")
        except Exception as e:
            print(f"❌ Önbellek yükleme hatası: {e}")
            self.events = []
    
    def get_events_by_city(self, city):
        """Belirtilen şehirdeki etkinlikleri filtrele ve döndür"""
        return [e for e in self.events if e.get('city') == city]
    
    def get_all_events(self, filter_past=True, filter_sources=True):
        """
        Tüm etkinlikleri döndür
        
        Args:
            filter_past: Geçmiş tarihli etkinlikleri filtrele (varsayılan: True)
            filter_sources: Sadece scraping yapılan kaynakları göster (varsayılan: True)
        
        Returns:
            list: Etkinlik listesi
        """
        events = self.events
        
        # 1. Kaynak filtresi (sadece resmi scraping kaynakları)
        if filter_sources:
            events = [e for e in events if e.get('source') in self.ALLOWED_SOURCES]
        
        # 2. Geçmiş tarih filtresi
        if not filter_past:
            return events
        
        today = datetime.now().date()
        upcoming_events = []
        
        for event in events:
            date_str = event.get('date', '')
            if not date_str:
                # Tarih bilgisi yoksa dahil et (Biletinial'den bazı etkinliklerde tarih yok)
                upcoming_events.append(event)
                continue
            
            try:
                event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if event_date >= today:
                    upcoming_events.append(event)
            except:
                # Tarih parse edilemezse dahil et
                upcoming_events.append(event)
        
        return upcoming_events
    
    def get_events_by_source(self, source):
        """Belirtilen kaynaktan (Biletinial, BUBilet) gelen etkinlikleri filtrele"""
        return [e for e in self.events if e.get('source') == source]
    
    def get_event_statistics(self):
        """Etkinlik istatistiklerini hesapla ve döndür"""
        return {
            'total_events': len(self.events),
            'kocaeli_count': len(self.get_events_by_city('Kocaeli')),
            'sakarya_count': len(self.get_events_by_city('Sakarya')),
            'sources': {
                'Biletix': len(self.get_events_by_source('Biletix')),
                'Biletinial': len(self.get_events_by_source('Biletinial')),
                'BUBilet': len(self.get_events_by_source('BUBilet')),
            }
        }

    # --- Tarih Bazlı Filtreleme ---
    def filter_by_date(self, target_date_str: str):
        """Belirli bir tarihteki etkinlikleri filtrele (YYYY-MM-DD formatında).
        Etkinlikte 'date' alanı yoksa veya parse edilemiyorsa, başlık ve konum
        metninden tarih çıkarmayı dener (base_scraper.parse_date_from_text ile).
        """
        from datetime import datetime
        target = None
        try:
            target = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except Exception:
            return []

        filtered = []
        # Tarih parse işlemi için BaseEventScraper örneği oluştur
        try:
            from data_scraper.base_scraper import BaseEventScraper
            parser = BaseEventScraper()
        except Exception:
            parser = None

        for e in self.events:
            date_text = (e.get('date') or '')
            iso_date = None
            # Eğer zaten 'YYYY-MM-DD' formatındaysa direkt kullan
            if isinstance(date_text, str) and len(date_text) == 10 and date_text[4] == '-' and date_text[7] == '-':
                iso_date = date_text
            elif parser is not None:
                # Başlık veya konum metninden tarih çıkarmayı dene
                iso_date = parser.parse_date_from_text(date_text) or \
                           parser.parse_date_from_text(e.get('title', '')) or \
                           parser.parse_date_from_text(e.get('location', ''))

            if not iso_date:
                continue
            try:
                d = datetime.strptime(iso_date, '%Y-%m-%d').date()
                if d == target:
                    filtered.append(e)
            except Exception:
                continue
        return filtered