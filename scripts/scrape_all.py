from data_scraper.event_manager import EventManager
import logging
import sys
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == '__main__':
    logging.info('Starting daily scrape')
    try:
        m = EventManager(use_cache=False)
        stats = m.get_event_statistics()
        logging.info(f"Scrape finished: {stats}")
    except Exception as e:
        logging.exception('Scrape failed')
        sys.exit(2)
    logging.info('Done')
