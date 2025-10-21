"""
BUBilet sitesinden etkinlik verisi çeken scraper
requests + BeautifulSoup kullanır (Selenium değil)
"""

import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .base_scraper import BaseEventScraper


class BUBiletScraper(BaseEventScraper):
    """BUBilet sitesi için özel scraper - requests/BeautifulSoup"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bubilet.com.tr"
        self.cache_file = "./data/cache/bubilet_events.json"
        
        # Hedef URL'ler
        self.target_urls = {
            'kocaeli': 'https://www.bubilet.com.tr/kocaeli',
            'sakarya': 'https://www.bubilet.com.tr/sakarya'
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
        """BUBilet'ten etkinlikleri çeker - requests/BeautifulSoup kullanır"""
        
        # Önce cache'den kontrol et
        cached_events = self.get_cache(self.cache_file)
        if cached_events:
            print("✅ BUBilet verisi cache'den alındı")
            return cached_events
        
        print("🔄 BUBilet'ten yeni veri çekiliyor...")
        
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
                    
                    # Etkinlik linklerini bul
                    event_links = soup.select("a[href*='/etkinlik/']")
                    print(f"   → {len(event_links)} etkinlik linki bulundu")
                    
                    seen_urls = set()
                    
                    for link in event_links:
                        try:
                            # Şehir mapping
                            city_map = {
                                'kocaeli': 'Kocaeli',
                                'sakarya': 'Sakarya'
                            }
                            
                            event_data = {
                                'title': '',
                                'date': '',
                                'time': '',
                                'location': '',
                                'city': city_map.get(url_key, url_key.title()),
                                'price': '',
                                'description': '',
                                'url': '',
                                'link': '',  # Link alanı eklendi (AI için)
                                'source': 'BUBilet'
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
                            
                            # Başlık (h3)
                            h3 = link.select_one("h3")
                            if h3:
                                event_data['title'] = self.clean_text(h3.get_text(" "))
                            
                            # Title from attribute fallback
                            if not event_data['title']:
                                title_attr = link.get('title')
                                if title_attr:
                                    event_data['title'] = self.clean_text(title_attr)
                            
                            # Yer ve Tarih (p tags)
                            p_tags = link.select("p.text-gray-500")
                            if len(p_tags) >= 1:
                                event_data['location'] = self.clean_text(p_tags[0].get_text(" "))
                            if len(p_tags) >= 2:
                                date_text = self.clean_text(p_tags[1].get_text(" "))
                                event_data['date'] = date_text
                                # Parse tarih ISO formatına
                                parsed = self.parse_date_from_text(date_text)
                                if parsed:
                                    event_data['date'] = parsed
                            
                            # Fiyat (span.tracking-tight)
                            price_span = link.select_one("span.tracking-tight")
                            if price_span:
                                price_text = self.clean_text(price_span.get_text(" "))
                                if price_text and not price_text.endswith('₺'):
                                    event_data['price'] = price_text + " ₺"
                                else:
                                    event_data['price'] = price_text
                            
                            # Ensure city and validate
                            event_data = self.ensure_city(event_data, url_key)
                            
                            if event_data['title'] and len(event_data['title']) > 3 and event_data['url']:
                                events.append(event_data)
                                print(f"   ✅ Etkinlik {len(events)}: {event_data['title'][:50]}...")
                        
                        except Exception as e:
                            continue
                
                except Exception as e:
                    print(f"   ❌ {url_key} çekilemedi: {e}")
        
        except Exception as e:
            print(f"❌ BUBilet scraping hatası: {e}")
        
        # Cache'e kaydet
        self.save_cache(events, self.cache_file)
        print(f"\n✅ BUBilet'ten {len(events)} etkinlik çekildi")
        
        return events
    
    def _has_lxml(self):
        """lxml kütüphanesinin yüklü olup olmadığını kontrol et"""
        try:
            import lxml
            return True
        except ImportError:
            return False
