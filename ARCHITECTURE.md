# Project Architecture

Generated: 2026-05-14 17:32:44
Root: `/Users/martina/PycharmProjects/PythonProject/ecommerce_price_tracker`

```
ecommerce_price_tracker/
├── data/
│   └── output/
│       ├── .gitkeep
│       ├── best_prices.csv  [7,343 bytes]
│       ├── latest_prices.csv  [45,379 bytes]
│       ├── price_history.csv  [1,340,567 bytes]
│       └── price_spread.csv  [3,129 bytes]
├── database/
│   └── schema.sql  [1,563 bytes]
├── docs/
│   ├── best_prices_sample_1.png  [751,777 bytes]
│   ├── google_sheets_preview.png  [894,321 bytes]
│   ├── google_sheets_preview_2.png  [1,019,077 bytes]
│   ├── google_sheets_preview_3.png  [557,146 bytes]
│   └── prices_sample_1.png  [1,054,498 bytes]
├── logs/
│   ├── .gitkeep
│   └── app.log  [309,018 bytes]
├── secrets/
│   └── google_service_account.json  [2,397 bytes]
├── src/
│   ├── analytics/
│   │   ├── best_prices.py  [2,237 bytes]
│   │   └── price_spread.py  [3,298 bytes]
│   ├── data/
│   │   └── output/
│   │       └── atkinsons_debug.html  [453,115 bytes]
│   ├── output/
│   │   ├── analytics_csv_writer.py  [757 bytes]
│   │   ├── csv_writer.py  [2,438 bytes]
│   │   ├── db.py  [3,983 bytes]
│   │   ├── db_writer.py  [2,284 bytes]
│   │   └── google_sheets.py  [2,469 bytes]
│   ├── processing/
│   │   ├── cleaner.py  [1,102 bytes]
│   │   ├── deduplicator.py  [809 bytes]
│   │   ├── product_metadata.py  [4,519 bytes]
│   │   ├── source_metadata.py  [400 bytes]
│   │   └── validator.py  [675 bytes]
│   ├── scraper/
│   │   ├── atkinsons_parser.py  [6,745 bytes]
│   │   ├── browser_fetcher.py  [1,122 bytes]
│   │   ├── bullionbypost_parser.py  [7,462 bytes]
│   │   ├── fetcher.py  [1,200 bytes]
│   │   ├── selectors.py
│   │   └── ukbullion_parser.py  [4,886 bytes]
│   ├── web/
│   │   ├── static/
│   │   │   └── style.css  [3,817 bytes]
│   │   ├── templates/
│   │   │   └── dashboard.html  [5,685 bytes]
│   │   └── app.py  [1,791 bytes]
│   ├── config.py  [988 bytes]
│   ├── logger.py  [885 bytes]
│   ├── main.py  [4,770 bytes]
│   ├── models.py
│   ├── sources.py  [2,175 bytes]
│   ├── sources_registry.py  [1,150 bytes]
│   └── test_atkinsons_parser.py  [1,043 bytes]
├── tests/
│   └── .gitkeep
├── .env  [303 bytes]
├── .env.example  [372 bytes]
├── .gitignore  [398 bytes]
├── ARCHITECTURE.md  [2,723 bytes]
├── check_session.sh  [357 bytes]
├── claud_test.py  [756 bytes]
├── print_architecture.py  [2,385 bytes]
├── README.md  [3,738 bytes]
├── requirements.txt  [412 bytes]
└── testic.py  [321 bytes]
```