"""
Book Scraper - A tool to scrape book information from books.toscrape.com
Features:
- Concurrent scraping using ThreadPoolExecutor
- Robust error handling and retries
- Progress tracking
- Detailed logging
- Rate limiting to be respectful to the server
"""

import concurrent.futures
import csv
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
MAX_RETRIES = 3
TIMEOUT = 10
MAX_WORKERS = 5
RATE_LIMIT = 1  # Minimum seconds between requests
OUTPUT_FILE = "books.csv"
LOG_FILE = "scraper.log"

@dataclass
class Book:
    """Data class to store book information"""
    title: str
    price: str
    availability: str
    rating: str
    url: str

class BookScraper:
    def __init__(self):
        # Set up logging
        self._setup_logging()
        
        # Configure session with retries and timeouts
        self.session = self._setup_session()
        
        # Track last request time for rate limiting
        self.last_request_time = 0

    def _setup_logging(self) -> None:
        """Configure logging settings"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler()
            ]
        )

    def _setup_session(self) -> requests.Session:
        """Configure requests session with retries and timeouts"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def _rate_limit(self) -> None:
        """Implement rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < RATE_LIMIT:
            time.sleep(RATE_LIMIT - elapsed)
        self.last_request_time = time.time()

    def scrape_page(self, page_number: int) -> List[Book]:
        """
        Scrape a single page of books
        
        Args:
            page_number: The page number to scrape
            
        Returns:
            List of Book objects
        
        Raises:
            requests.RequestException: If the page cannot be retrieved
        """
        self._rate_limit()
        url = BASE_URL.format(page_number)
        logging.info(f"Scraping page {page_number}")
        
        try:
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            books = []
            
            for book in soup.find_all('article', class_='product_pod'):
                try:
                    books.append(Book(
                        title=book.h3.a['title'],
                        price=book.find(class_='price_color').text,
                        availability=book.find(class_='instock availability').text.strip(),
                        rating=book.find(class_='star-rating')['class'][1],
                        url=book.h3.a['href']
                    ))
                except (AttributeError, KeyError) as e:
                    logging.error(f"Error parsing book on page {page_number}: {e}")
                    continue
            
            return books
            
        except requests.RequestException as e:
            logging.error(f"Error scraping page {page_number}: {e}")
            raise

    def save_books(self, books: List[Book], filename: str) -> None:
        """Save books to CSV file"""
        fieldnames = ['title', 'price', 'availability', 'rating', 'url']
        
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for book in books:
                writer.writerow(book.__dict__)

    def scrape_all_pages(self, start_page: int = 1, end_page: int = 50) -> List[Book]:
        """Scrape multiple pages concurrently"""
        all_books = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_page = {
                executor.submit(self.scrape_page, page_number): page_number
                for page_number in range(start_page, end_page + 1)
            }
            
            for future in concurrent.futures.as_completed(future_to_page):
                page_number = future_to_page[future]
                try:
                    page_books = future.result()
                    all_books.extend(page_books)
                    logging.info(f"Completed page {page_number}, found {len(page_books)} books")
                except Exception as e:
                    logging.error(f"Page {page_number} generated an exception: {e}")
        
        return all_books

def main():
    """Main entry point"""
    try:
        scraper = BookScraper()
        logging.info("Starting book scraping")
        
        books = scraper.scrape_all_pages()
        logging.info(f"Total books scraped: {len(books)}")
        
        scraper.save_books(books, OUTPUT_FILE)
        logging.info(f"Data saved to {OUTPUT_FILE}")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()