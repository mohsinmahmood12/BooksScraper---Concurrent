# Web Scraper

This script concurrently scrapes data from a website https://books.toscrape.com/ and saves it to a CSV file. The website should list books and include the following information for each book: title, price, availability, and rating.

## Getting Started

Install the required packages: concurrent.futures, csv, and requests.
```
    pip install concurrent.futures
    pip install csv
    pip install requests

 ```
Set the URL_template variable to the URL of the website you want to scrape. The website should use a similar pagination format as the example given (i.e. https://books.toscrape.com/catalogue/page-{}.html).
Run the script. It will scrape the website and save the data in a CSV file called books.csv.
## Functionality

The scrape_page function takes in a page number and returns a list of dictionaries containing information about the books on that page. The script then uses a ThreadPoolExecutor to create a thread pool and submit tasks to scrape each page concurrently. As the tasks complete, their results are written to the CSV file using a DictWriter object.

## Built With

Python 3 - The programming language used
Beautiful Soup - The library used for parsing HTML and XML
concurrent.futures - The library used for concurrent execution of function calls
csv - The library used for reading and writing CSV files
requests - The library used for sending HTTP requests
## Author

Mohsin Mehmood