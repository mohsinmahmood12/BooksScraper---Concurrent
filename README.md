# Books.ToScrape Scraper

A high-performance, concurrent web scraper for books.toscrape.com built with Python. Features robust error handling, rate limiting, and detailed logging while respecting the website's resources.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🚀 Concurrent scraping using ThreadPoolExecutor
- 📊 Automatic CSV export
- 🔄 Smart retry mechanism
- ⏱️ Rate limiting to respect server resources
- 📝 Comprehensive logging
- 🛡️ Robust error handling

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/books-scraper.git
cd books-scraper
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

Basic usage:
```bash
python scraper.py
```

With custom parameters:
```bash
python scraper.py --pages 100 --workers 5 --output books.csv
```

## Configuration

Key settings in `scraper.py`:

```python
MAX_RETRIES = 3        # Maximum retry attempts
TIMEOUT = 10           # Request timeout in seconds
MAX_WORKERS = 5        # Concurrent threads
RATE_LIMIT = 1         # Seconds between requests
OUTPUT_FILE = "books.csv"
```

## Output Format

The scraper saves data in CSV format with the following columns:

| Column | Description |
|--------|-------------|
| title | Book title |
| price | Price in £ |
| availability | Stock status |
| rating | Star rating (1-5) |
| url | Book detail page URL |

## Advanced Features

### Logging

- Detailed logs saved to `scraper.log`
- Console output for progress tracking
- Error tracking and reporting

### Error Handling

- Automatic retry for failed requests
- Rate limit detection and handling
- Malformed HTML protection
- Network error recovery

### Performance

- Concurrent page processing
- Connection pooling
- Session reuse
- Optimized memory usage

## Development

### Project Structure
```
├── scraper.py         # Main scraper code
├── README.md         # Documentation
└── .gitignore       # Git ignore file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Dependencies

- requests>=2.26.0
- beautifulsoup4>=4.9.3
- urllib3>=1.26.7

## Troubleshooting

Common issues and solutions:

1. Rate limiting:
   - Increase `RATE_LIMIT` value
   - Reduce `MAX_WORKERS`

2. Connection errors:
   - Check internet connection
   - Verify website availability
   - Increase `TIMEOUT` value

## Acknowledgments

- [Books to Scrape](https://books.toscrape.com/) for providing the test website
- BeautifulSoup4 developers for the excellent parsing library
- Python community for the concurrent.futures framework

---

**Note**: This scraper is for educational purposes only. Always check and respect a website's robots.txt and terms of service before scraping.