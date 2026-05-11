# Gold Coin Price Tracker

> This project is based on a real-world use case: tracking and comparing gold coin prices across UK bullion dealers.
> The goal was to build an automated pipeline that scrapes live prices, normalises the data, and surfaces the best deals — updated on every run.

---

## What This Project Does

Fetches gold coin listings from multiple UK dealers, normalises the data, and outputs:

- the **cheapest price per coin** across all dealers
- **price spreads** showing how much prices vary for the same coin
- a **90-day price history** for trend analysis

All results are exported to CSV files and synced to Google Sheets automatically.

---

## Problem Context

Gold coin prices change constantly and vary significantly between dealers.
Comparing them manually across multiple websites is slow and error-prone.

This project automates that process end-to-end:

- some dealers load prices dynamically via private APIs — not visible in plain HTML
- the same product often appears on multiple listing pages with different URLs
- product names are inconsistent across dealers (e.g. "1 Ounce", "1oz", "1 OZ" all mean the same thing)
- bulk items, proof sets, and collectibles need to be filtered out before any price comparison makes sense

The project focuses on handling these real-world messy scenarios, not clean datasets.

---

## How It Works

```
Fetch HTML / API  →  Parse raw records  →  Deduplicate
→  Validate  →  Enrich (weight, year, coin_family, price_per_oz)
→  Filter (bulk, proof, pre-owned)  →  Analytics  →  CSV + Google Sheets
```

Step-by-step:

- fetch HTML from listing pages (HTTP or browser-based via Playwright)
- for dealers with dynamic pricing — identify product IDs from HTML, then fetch all prices in one POST request to the live pricing API
- parse product name, URL, availability per card
- extract metadata from product names using regex: weight, year, coin family
- deduplicate using `dealer + url slug` — same product can appear across multiple listing pages
- filter out non-comparable items: tubes, boxes, sets, proof, graded, pre-owned
- find best price and price spread per coin group
- write to CSV and sync to Google Sheets

---

## Output Files

| File | Description |
|---|---|
| `latest_prices.csv` | All current prices from all dealers |
| `price_history.csv` | Rolling 90-day price history |
| `best_prices.csv` | Cheapest price per coin group |
| `price_spread.csv` | Min/max spread per coin group across dealers |

---

## Tech Stack

- Python
- `requests`, `BeautifulSoup4`, `Playwright`
- `gspread`, `google-auth`
- `python-dotenv`
- CSV, logging with rotation

---

## What This Project Demonstrates

- reverse engineering of private dealer APIs for live pricing
- multi-source scraper architecture — each dealer is a self-contained module
- regex-based metadata extraction from inconsistent product names
- deduplication across listing pages with different URLs
- data quality controls: validation, field warnings, exclusion logic
- Google Sheets automation via API
- production-ready logging, retry logic, and error handling

---

## Run Locally

```bash
git clone <repo>
cd ecommerce_price_tracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# fill in your Google Sheets credentials

python src/main.py
```

---

## About Me

I build practical automation tools focused on:
- web scraping
- data extraction
- eCommerce automation