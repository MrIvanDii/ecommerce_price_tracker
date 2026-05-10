# Project Architecture

Generated: 2026-05-10 12:28:33
Root: `/Users/martina/PycharmProjects/PythonProject/ecommerce_price_tracker`

```
ecommerce_price_tracker/
├── data/
│   └── output/
│       ├── .gitkeep
│       ├── best_prices.csv  [4,799 bytes]
│       ├── latest_prices.csv  [61,599 bytes]
│       ├── price_history.csv  [1,838,679 bytes]
│       └── price_spread.csv  [3,530 bytes]
├── logs/
│   ├── .gitkeep
│   └── app.log  [245,043 bytes]
├── secrets/
│   └── google_service_account.json  [2,397 bytes]
├── src/
│   ├── analytics/
│   │   ├── best_prices.py  [1,809 bytes]
│   │   └── price_spread.py  [2,923 bytes]
│   ├── data/
│   │   └── output/
│   │       └── atkinsons_debug.html  [453,115 bytes]
│   ├── output/
│   │   ├── analytics_csv_writer.py  [757 bytes]
│   │   ├── csv_writer.py  [1,135 bytes]
│   │   └── google_sheets.py  [2,469 bytes]
│   ├── processing/
│   │   ├── cleaner.py  [1,102 bytes]
│   │   ├── deduplicator.py  [336 bytes]
│   │   ├── product_metadata.py  [2,775 bytes]
│   │   ├── source_metadata.py  [400 bytes]
│   │   └── validator.py  [675 bytes]
│   ├── scraper/
│   │   ├── atkinsons_parser.py  [6,745 bytes]
│   │   ├── browser_fetcher.py  [1,122 bytes]
│   │   ├── bullionbypost_parser.py  [7,462 bytes]
│   │   ├── fetcher.py  [401 bytes]
│   │   ├── selectors.py
│   │   └── ukbullion_parser.py  [4,724 bytes]
│   ├── config.py  [502 bytes]
│   ├── logger.py  [677 bytes]
│   ├── main.py  [4,501 bytes]
│   ├── models.py
│   ├── sources.py  [2,175 bytes]
│   ├── sources_registry.py  [1,150 bytes]
│   └── test_atkinsons_parser.py  [1,043 bytes]
├── tests/
│   └── .gitkeep
├── .env  [141 bytes]
├── .gitignore  [375 bytes]
├── claud_test.py  [1,411 bytes]
├── print_architecture.py  [2,385 bytes]
├── README.md
└── requirements.txt  [412 bytes]
```