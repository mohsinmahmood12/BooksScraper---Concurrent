import concurrent.futures
import csv
import requests
from bs4 import BeautifulSoup

URL_template = "https://books.toscrape.com/catalogue/page-{}.html"

def scrape_page(page_number):
    URL = URL_template.format(page_number)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    books = soup.find_all('article')
    
    page_data = []
    for book in books:
        title = book.find('h3').text
        price = book.find(class_='price_color').text
        availability = book.find(class_='instock availability').text.strip()
        rating = book.find(class_='star-rating')['class'][1]
        
        page_data.append({'title': title, 'price': price, 'availability': availability, 'rating': rating})
    
    return page_data

with concurrent.futures.ThreadPoolExecutor() as executor:
    with open('books.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'price', 'availability', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        futures = [executor.submit(scrape_page, page_number) for page_number in range(1, 51)]
        
        for future in concurrent.futures.as_completed(futures):
            page_data = future.result()
            for book in page_data:
                writer.writerow(book)
