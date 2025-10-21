"""
Biletinial sitesinden etkinlik verisi çeken scraper
requests + BeautifulSoup kullanır (Selenium değil)
"""

import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .base_scraper import BaseEventScraper


class BiletinialScraper(BaseEventScraper):
    """Biletinial sitesi için özel scraper - requests/BeautifulSoup"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://biletinial.com"
        self.cache_file = "./data/cache/biletinial_events.json"
        
        # Hedef URL'ler - Spesifik etkinlik sayfaları
        self.target_urls = {
            'kocaeli_sinema': 'https://biletinial.com/tr-tr/sinema/kocaeli',
            'kocaeli_events': 'https://biletinial.com/tr-tr/sehrineozel/kocaeli',
            'sakarya_sinema': 'https://biletinial.com/tr-tr/sinema/sakarya',
            'sakarya_events': 'https://biletinial.com/tr-tr/sehrineozel/sakarya'
        }
        
        # HTTP Headers
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }
    
    def scrape_events(self):
        """Biletinial'ten etkinlikleri çeker - requests/BeautifulSoup kullanır"""
        
        # Önce cache'den kontrol et
        cached_events = self.get_cache(self.cache_file)
        if cached_events:
            print("✅ Biletinial verisi cache'den alındı")
            return cached_events
        
        print("🔄 Biletinial'ten yeni veri çekiliyor...")
        
        session = requests.Session()
        session.headers.update(self.headers)
        
        events = []
        
        try:
            for url_key, url in self.target_urls.items():
                print(f"\n📡 {url_key} çekiliyor: {url}")
                
                try:
                    # HTTP request
                    response = session.get(url, timeout=20)
                    response.raise_for_status()
                    
                    # BeautifulSoup ile parse
                    parser = "lxml" if self._has_lxml() else "html.parser"
                    soup = BeautifulSoup(response.text, parser)
                    
                    # Farklı selektörleri dene
                    selectors = [
                        "a[href*='/tiyatro/']",
                        "a[href*='/sinema/']",
                        "a[href*='/etkinlik/']",
                    ]
                    
                    found_links = []
                    for selector in selectors:
                        links = soup.select(selector)
                        if links:
                            found_links.extend(links)
                    
                    print(f"   → {len(found_links)} etkinlik linki bulundu")
                    
                    # Deduplicate by URL
                    seen_urls = set()
                    
                    for link in found_links[:30]:  # İlk 30 link
                        try:
                            # Şehir mapping
                            city_map = {
                                'kocaeli_sinema': 'Kocaeli',
                                'kocaeli_events': 'Kocaeli',
                                'sakarya_sinema': 'Sakarya',
                                'sakarya_events': 'Sakarya'
                            }
                            
                            event_data = {
                                'title': '',
                                'date': '',
                                'time': '',
                                'location': '',
                                'city': city_map.get(url_key, ''),
                                'price': '',
                                'description': '',
                                'url': '',
                                'link': '',  # Link alanı eklendi (AI için)
                                'source': 'Biletinial'
                            }
                            
                            # URL
                            href = link.get('href')
                            if href:
                                full_url = href if href.startswith('http') else urljoin(self.base_url, href)
                                event_data['url'] = full_url
                                event_data['link'] = full_url  # Link alanını da doldur
                                if event_data['url'] in seen_urls:
                                    continue
                                seen_urls.add(event_data['url'])
                            
                            # Başlık
                            event_data['title'] = self.clean_text(link.get_text(" ")) or self.clean_text(link.get('title', ''))
                            
                            # Başlık arama - farklı tag'lerde olabilir
                            if not event_data['title']:
                                title_selectors = ['h3', 'h4', 'h5', '.title', '[class*="title"]']
                                for sel in title_selectors:
                                    title_el = link.select_one(sel)
                                    if title_el:
                                        event_data['title'] = self.clean_text(title_el.get_text(" "))
                                        break
                            
                            # Ensure city
                            event_data = self.ensure_city(event_data, url_key)
                            
                            if event_data['title'] and len(event_data['title']) > 3 and event_data['url']:
                                # Gereksiz linkleri filtrele
                                if any(skip in event_data['title'].lower() for skip in ['tümünü', 'müşteri hizmet', 'keşfet']):
                                    continue
                                events.append(event_data)
                                print(f"   ✅ Etkinlik {len(events)}: {event_data['title'][:50]}...")
                        
                        except Exception:
                            continue
                
                except Exception as e:
                    print(f"   ❌ {url_key} çekilemedi: {e}")
        
        except Exception as e:
            print(f"❌ Biletinial scraping hatası: {e}")
        
        # Cache'e kaydet
        self.save_cache(events, self.cache_file)
        print(f"\n✅ Biletinial'ten {len(events)} etkinlik çekildi")
        
        return events
    
    def _has_lxml(self):
        """lxml kütüphanesinin yüklü olup olmadığını kontrol et"""
        try:
            import lxml
            return True
        except ImportError:
            return False
    
    def extract_event_data(self, card_element):
        """Etkinlik kartından veri çıkarır"""
        event_data = {
            'title': '',
            'date': '',
            'time': '',
            'location': '',
            'city': '',
            'price': '',
            'description': '',
            'url': '',
            'link': '',  # Link alanı eklendi (AI için)
            'source': 'Biletinial'
        }
        
        try:
            # URL'yi al
            try:
                href = card_element.get_attribute('href')
                if href:
                    full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                    event_data['url'] = full_url
                    event_data['link'] = full_url  # Link alanını da doldur
            except:
                pass
            
            # Kartın tüm metnini al
            all_text = self.clean_text(card_element.text)
            print(f"      Kart metni: {all_text[:100]}...")
            
            # Metni satırlara böl
            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
            
            if lines:
                # İlk satır genellikle başlık
                event_data['title'] = lines[0]
                
                # Diğer satırları analiz et
                for line in lines[1:]:
                    line_lower = line.lower()
                    
                    # Tarih formatı kontrolü
                    date_keywords = ['paz', 'pzt', 'sal', 'çrş', 'per', 'cum', 'cmt', 'ocak', 'şubat', 'mart', 'nisan', 'mayıs', 'haziran', 'temmuz', 'ağustos', 'eylül', 'ekim', 'kasım', 'aralık']
                    if any(word in line_lower for word in date_keywords):
                        if not event_data['date']:
                            event_data['date'] = line
                        elif not event_data['time'] and (':' in line or any(word in line_lower for word in ['paz', 'pzt', 'sal', 'çrş', 'per', 'cum', 'cmt'])):
                            event_data['time'] = line
                    
                    # Fiyat formatı kontrolü
                    elif '₺' in line or 'tl' in line_lower or ('tükendi' in line_lower):
                        if not event_data['price']:
                            event_data['price'] = line
                    
                    # Konum kontrolü
                    else:
                        location_keywords = ['kocaeli', 'sakarya', 'izmit', 'adapazarı', 'sinema', 'tiyatro', 'konser', 'merkez', 'salon']
                        if any(word in line_lower for word in location_keywords):
                            if not event_data['location']:
                                event_data['location'] = line
                                
                                # Şehir bilgisini çıkar
                                if any(city in line_lower for city in ['kocaeli', 'izmit']):
                                    event_data['city'] = 'Kocaeli'
                                elif any(city in line_lower for city in ['sakarya', 'adapazarı']):
                                    event_data['city'] = 'Sakarya'
            
            # Eğer şehir bulunamazsa, URL'den çıkar
            if not event_data['city']:
                if '/kocaeli' in event_data['url'].lower():
                    event_data['city'] = 'Kocaeli'
                elif '/sakarya' in event_data['url'].lower():
                    event_data['city'] = 'Sakarya'
            
            # Eğer konum bulunamazsa, şehir bilgisini kullan
            if not event_data['location']:
                event_data['location'] = event_data['city']
            
            print(f"      Çıkarılan veri: {event_data['title'][:30]}... | {event_data['date']} | {event_data['price']}")
            
        except Exception as e:
            print(f"❌ Etkinlik verisi çıkarılırken hata: {e}")
        
        # En az başlık varsa etkinliği kabul et
        return event_data if event_data['title'] and len(event_data['title']) > 3 else None