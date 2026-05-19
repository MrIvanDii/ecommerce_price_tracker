# Project Architecture

Generated: 2026-05-19 20:17:55
Root: `/Users/martina/PycharmProjects/PythonProject/ecommerce_price_tracker`

```
ecommerce_price_tracker/
├── data/
│   └── output/
│       ├── .gitkeep
│       ├── best_prices.csv  [12,047 bytes]
│       ├── latest_prices.csv  [53,972 bytes]
│       ├── price_history.csv  [2,301,521 bytes]
│       └── price_spread.csv  [6,448 bytes]
├── database/
│   └── schema.sql  [1,472 bytes]
├── docs/
│   ├── best_prices_sample_1.png  [751,777 bytes]
│   ├── google_sheets_preview.png  [894,321 bytes]
│   ├── google_sheets_preview_2.png  [1,019,077 bytes]
│   ├── google_sheets_preview_3.png  [557,146 bytes]
│   └── prices_sample_1.png  [1,054,498 bytes]
├── logs/
│   ├── .gitkeep
│   └── app.log  [453,967 bytes]
├── secrets/
│   └── google_service_account.json  [2,397 bytes]
├── src/
│   ├── analytics/
│   │   ├── best_prices.py  [2,413 bytes]
│   │   └── price_spread.py  [3,300 bytes]
│   ├── data/
│   │   └── output/
│   │       └── atkinsons_debug.html  [453,115 bytes]
│   ├── output/
│   │   ├── analytics_csv_writer.py  [757 bytes]
│   │   ├── csv_writer.py  [2,438 bytes]
│   │   ├── db.py  [3,815 bytes]
│   │   ├── db_writer.py  [2,303 bytes]
│   │   └── google_sheets.py  [2,469 bytes]
│   ├── processing/
│   │   ├── cleaner.py  [1,102 bytes]
│   │   ├── deduplicator.py  [809 bytes]
│   │   ├── product_metadata.py  [4,694 bytes]
│   │   ├── source_metadata.py  [400 bytes]
│   │   └── validator.py  [675 bytes]
│   ├── scraper/
│   │   ├── acl_parser.py  [3,995 bytes]
│   │   ├── atkinsons_parser.py  [6,745 bytes]
│   │   ├── browser_fetcher.py  [1,122 bytes]
│   │   ├── bullionbypost_parser.py  [7,462 bytes]
│   │   ├── fetcher.py  [1,200 bytes]
│   │   ├── royalmint_parser.py  [5,464 bytes]
│   │   ├── selectors.py
│   │   └── ukbullion_parser.py  [4,886 bytes]
│   ├── web/
│   │   ├── static/
│   │   │   └── style.css  [3,817 bytes]
│   │   ├── templates/
│   │   │   └── dashboard.html  [5,685 bytes]
│   │   └── app.py  [1,834 bytes]
│   ├── config.py  [814 bytes]
│   ├── logger.py  [885 bytes]
│   ├── main.py  [7,039 bytes]
│   ├── models.py
│   ├── sources.py  [2,578 bytes]
│   ├── sources_registry.py  [1,697 bytes]
│   └── test_atkinsons_parser.py  [1,043 bytes]
├── tests/
│   └── .gitkeep
├── .env  [438 bytes]
├── .env.example  [372 bytes]
├── .gitignore  [414 bytes]
├── ARCHITECTURE.md  [3,224 bytes]
├── check_session.sh  [357 bytes]
├── claud_test.py  [756 bytes]
├── print_architecture.py  [2,385 bytes]
├── README.md  [3,738 bytes]
├── render.yaml  [365 bytes]
├── render_dump.sql  [137,710 bytes]
├── requirements.txt  [457 bytes]
└── testic.py  [321 bytes]
```