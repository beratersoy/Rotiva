"""
Biletix sitesinden etkinlik verisi çeken scraper
"""

import time
import re
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_scraper import BaseEventScraper


class BiletixScraper(BaseEventScraper):
    """Biletix sitesi için özel scraper"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.biletix.com"
        self.cache_file = "./data/cache/biletix_events.json"
        
        # Hedef URL'ler - Kocaeli ve Sakarya için özel arama sayfaları
        self.target_urls = {
            'kocaeli_search': 'https://www.biletix.com/search/TURKIYE/tr?category_sb=-1&date_sb=-1&city_sb=Kocaeli#!city_sb:Kocaeli',
            'sakarya_search': 'https://www.biletix.com/search/TURKIYE/tr?category_sb=-1&date_sb=-1&city_sb=Sakarya#!city_sb:Sakarya'
        }
        
    def scrape_events(self) -> List[Dict]:
        """Biletix'ten etkinlikleri çeker"""
        
        # Önce cache'den kontrol et
        cached_events = self.get_cache(self.cache_file)
        if cached_events:
            print("Biletix verisi cache'den alındı")
            return cached_events
        
        print("Biletix'ten yeni veri çekiliyor...")
        
        driver = self.setup_driver()
        events = []
        
        try:
            # Kocaeli arama sayfasına git
            kocaeli_url = self.target_urls['kocaeli_search']
            print(f"Kocaeli arama sayfasına gidiliyor: {kocaeli_url}")
            driver.get(kocaeli_url)
            
            # Sayfa yüklenmesini bekle
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("Sayfa yüklendi, dinamik içerik bekleniyor...")
            time.sleep(15)  # Daha uzun bekleme
            
            # Sayfayı kademeli scroll et (lazy loading için)
            print("Sayfa scroll ediliyor...")
            for i in range(5):
                driver.execute_script(f"window.scrollTo(0, {(i+1) * 800});")
                time.sleep(2)
            
            # Son scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            
            # Etkinlik kartlarını bul
            event_cards = driver.find_elements(By.CSS_SELECTOR, ".flexibleEvent")
            
            if not event_cards:
                # Alternatif selektörler dene
                event_cards = driver.find_elements(By.CSS_SELECTOR, 
                    ".searchResultEvent, .listevent, .event, .card, .item")
            
            print(f"Bulunan etkinlik kartı sayısı: {len(event_cards)}")
            
            # Her kartın içeriğini kontrol et
            valid_cards = []
            for i, card in enumerate(event_cards):
                try:
                    # Kartın içeriğini kontrol et
                    card_html = card.get_attribute('innerHTML')
                    if card_html and len(card_html.strip()) > 50:  # En az 50 karakter içerik
                        valid_cards.append(card)
                        print(f"Kart {i+1}: İçerik bulundu ({len(card_html)} karakter)")
                    else:
                        print(f"Kart {i+1}: Boş içerik")
                except Exception as e:
                    print(f"Kart {i+1}: Kontrol hatası - {e}")
            
            print(f"İçerikli kart sayısı: {len(valid_cards)}")
            
            # İçerikli kartlardan veri çıkar
            for i, card in enumerate(valid_cards[:20]):  # İlk 20 geçerli etkinliği al
                try:
                    print(f"Etkinlik {i+1} çıkarılıyor...")
                    event_data = self.extract_event_data(card)
                    if event_data and self.is_target_city(event_data):
                        events.append(event_data)
                        print(f"✅ Etkinlik {i+1}: {event_data['title'][:50]}...")
                    else:
                        print(f"❌ Etkinlik {i+1}: Veri çıkarılamadı")
                        
                except Exception as e:
                    print(f"❌ Etkinlik {i+1} çıkarılırken hata: {e}")
                    continue
            
            # Cache'e kaydet
            self.save_cache(events, self.cache_file)
            
        except Exception as e:
            print(f"Biletix scraping hatası: {e}")
        finally:
            driver.quit()
        
        print(f"Biletix'ten {len(events)} etkinlik çekildi")
        return events
    
    def extract_event_data(self, card_element) -> Dict:
        """Etkinlik kartından veri çıkarır"""
        event_data = {
            'title': '',
            'date': '',
            'time': '',
            'location': '',
            'city': 'Kocaeli',  # Varsayılan olarak Kocaeli
            'price': '',
            'description': '',
            'url': '',
            'source': 'Biletix'
        }
        
        try:
            # Önce kartın tüm metnini al
            all_text = self.clean_text(card_element.text)
            print(f"Kart metni: {all_text[:100]}...")
            
            # Başlık - Daha geniş selektörler
            title_selectors = [
                '.event-title', '.title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                '[data-testid*="title"]', '.event-name', '.name', '.heading',
                'a[href*="/etkinlik/"]', 'a[href*="/event/"]'
            ]
            
            for selector in title_selectors:
                try:
                    title_elem = card_element.find_element(By.CSS_SELECTOR, selector)
                    title_text = self.clean_text(title_elem.text)
                    if title_text and len(title_text) > 3:
                        event_data['title'] = title_text
                        print(f"Başlık bulundu: {title_text[:50]}...")
                        break
                except NoSuchElementException:
                    continue
            
            # Eğer başlık bulunamazsa, link metnini kullan
            if not event_data['title']:
                try:
                    link_elem = card_element.find_element(By.TAG_NAME, 'a')
                    link_text = self.clean_text(link_elem.text)
                    if link_text and len(link_text) > 3:
                        event_data['title'] = link_text
                        print(f"Link metni başlık olarak kullanıldı: {link_text[:50]}...")
                except NoSuchElementException:
                    pass
            
            # Tarih - Daha geniş selektörler
            date_selectors = [
                '.event-date', '.date', '.event-time', '.time', '.datetime',
                '[data-testid*="date"]', '.tarih', '.tarih-saat'
            ]
            
            for selector in date_selectors:
                try:
                    date_elem = card_element.find_element(By.CSS_SELECTOR, selector)
                    date_text = self.clean_text(date_elem.text)
                    if date_text:
                        event_data['date'] = date_text
                        print(f"Tarih bulundu: {date_text}")
                        break
                except NoSuchElementException:
                    continue
            
            # Konum - Daha geniş selektörler
            location_selectors = [
                '.event-location', '.location', '.venue', '.place', '.mekan',
                '[data-testid*="location"]', '.adres', '.yer'
            ]
            
            for selector in location_selectors:
                try:
                    location_elem = card_element.find_element(By.CSS_SELECTOR, selector)
                    location_text = self.clean_text(location_elem.text)
                    if location_text:
                        event_data['location'] = location_text
                        print(f"Konum bulundu: {location_text}")
                        break
                except NoSuchElementException:
                    continue
            
            # Fiyat - Daha geniş selektörler
            price_selectors = [
                '.event-price', '.price', '.ticket-price', '.fiyat', '.cost',
                '[data-testid*="price"]', '.amount', '.fee'
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = card_element.find_element(By.CSS_SELECTOR, selector)
                    price_text = self.clean_text(price_elem.text)
                    if price_text:
                        event_data['price'] = price_text
                        print(f"Fiyat bulundu: {price_text}")
                        break
                except NoSuchElementException:
                    continue
            
            # URL
            try:
                link_elem = card_element.find_element(By.TAG_NAME, 'a')
                href = link_elem.get_attribute('href')
                if href:
                    event_data['url'] = href if href.startswith('http') else f"{self.base_url}{href}"
                    print(f"URL bulundu: {event_data['url']}")
            except NoSuchElementException:
                pass
            
            # Eğer hiçbir şey bulunamazsa, kartın tüm metnini analiz et
            if not event_data['title'] and all_text:
                # Basit metin analizi ile başlık çıkar
                lines = [line.strip() for line in all_text.split('\n') if line.strip()]
                if lines:
                    # En uzun satırı başlık olarak kullan
                    event_data['title'] = max(lines, key=len)
                    print(f"Metin analizi ile başlık: {event_data['title'][:50]}...")
            
        except Exception as e:
            print(f"Etkinlik verisi çıkarılırken hata: {e}")
        
        # En az başlık varsa etkinliği kabul et
        return event_data if event_data['title'] and len(event_data['title']) > 3 else None