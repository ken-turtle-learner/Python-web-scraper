# Python Web Scraper — books.toscrape.com → Supabase

A Python ETL pipeline that scrapes book data from [books.toscrape.com](https://books.toscrape.com),
applies deduplication logic, and loads structured records into a Supabase database.

Built as a learning project to practice web scraping, pagination handling,
environment-based credential management, and database integration using Python.

---

## What It Does

1. **Extract** — Iterates through all paginated index pages on books.toscrape.com
   until a 404 is returned, collecting book data at each step
2. **Transform** — Parses HTML with BeautifulSoup, extracts structured fields,
   and filters out records that already exist in the database
3. **Load** — Inserts new records in bulk into a Supabase table

---

## Two Scripts

### `webscraper.py` — Full Detail Scraper
A two-pass approach. First pass collects links to all individual book pages from
the index. Second pass visits each book page to extract detailed data.

Stores to: `detailed_books` table

| Field | Description |
|---|---|
| `upc` | Universal Product Code — used as unique identifier |
| `title` | Book title |
| `price` | Price (£ symbol stripped) |
| `availability` | Stock status |

### `webscraper lite.py` — Single-Pass Scraper
Extracts all available data directly from the index pages in a single pass.
Faster to run, less detail per book.

Stores to: `books` table

| Field | Description |
|---|---|
| `link` | Book URL — used as unique identifier |
| `title` | Book title |
| `price` | Price (£ symbol stripped) |
| `rating` | Star rating (word form e.g. "Three") |
| `availability` | Stock status |

---

## Tech Stack

- Python 3
- [Requests](https://pypi.org/project/requests/) — HTTP requests
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) + lxml — HTML parsing
- [supabase-py](https://pypi.org/project/supabase/) — Supabase client
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management
- Python `logging` — Debug output and execution tracking

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/ken-turtle-learner/Python-web-scraper.git
cd Python-web-scraper
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4 lxml supabase python-dotenv
```

### 3. Create a `.env` file

Create a `.env` file in the project root with your Supabase credentials:
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

hese values are available in your Supabase project under **Settings > API**.

### 4. Set up the Supabase tables

For `webscraper.py`, create a `detailed_books` table with columns:
`upc` (text, primary key), `title` (text), `price` (text), `availability` (text)

For `webscraper lite.py`, create a `books` table with columns:
`link` (text, primary key), `title` (text), `price` (text), `rating` (text), `availability` (text)

### 5. Run

```bash
python webscraper.py
# or
python "webscraper lite.py"
```
## Planned Improvements

- [ ] Add `try/except` blocks around HTTP requests and Supabase inserts
- [ ] Fix UPC deduplication logic in `webscraper.py`
- [ ] Refactor flat code into functions
- [ ] Add a `requirements.txt`
- [ ] Add rate limiting / politeness delay between requests

---
