"""
Kocaeli & Sakarya Festival Chatbotu - Veri Çekme Modülü
Bu modül web sitelerinden etkinlik verilerini çeker ve yönetir

İçerik:
- BaseEventScraper: Tüm scraper'lar için temel sınıf
- BiletixScraper: Biletix sitesinden veri çeken sınıf
- BiletinialScraper: Biletinial sitesinden veri çeken sınıf
- EventManager: Tüm etkinlik verilerini koordine eden ana sınıf
"""

# Temel scraper sınıfını import et
from .base_scraper import BaseEventScraper

# Site-specific scraper'ları import et
from .biletix_scraper import BiletixScraper
from .biletinial_scraper import BiletinialScraper
from .bubilet_scraper import BUBiletScraper

# Ana veri yöneticisini import et
from .event_manager import EventManager

# Bu modülden export edilecek sınıflar
__all__ = [
    'BaseEventScraper',    # Temel scraper sınıfı
    'BiletixScraper',      # Biletix scraper'ı
    'BiletinialScraper',   # Biletinial scraper'ı
    'BUBiletScraper',      # BUBilet scraper'ı
    'EventManager'         # Ana veri yöneticisi
]
