-- price_latest: current snapshot (truncated on each run)
CREATE TABLE IF NOT EXISTS price_latest (
    id              SERIAL PRIMARY KEY,
    timestamp       TIMESTAMP,
    dealer          VARCHAR(100),
    product_name_clean VARCHAR(500),
    coin_family     VARCHAR(100),
    year            VARCHAR(10),
    weight          VARCHAR(50),
    price           NUMERIC(12, 2),
    price_per_oz    NUMERIC(12, 2),
    currency        VARCHAR(10),
    availability    BOOLEAN,
    listing_url     TEXT
);

-- price_history: rolling 90-day history
CREATE TABLE IF NOT EXISTS price_history (
    id              SERIAL PRIMARY KEY,
    created_at      TIMESTAMP DEFAULT NOW(),
    timestamp       TIMESTAMP,
    dealer          VARCHAR(100),
    product_name_clean VARCHAR(500),
    coin_family     VARCHAR(100),
    year            VARCHAR(10),
    weight          VARCHAR(50),
    price           NUMERIC(12, 2),
    price_per_oz    NUMERIC(12, 2),
    currency        VARCHAR(10),
    availability    BOOLEAN,
    listing_url     TEXT
);

-- price_best: best price per coin/weight group
CREATE TABLE IF NOT EXISTS price_best (
    id              SERIAL PRIMARY KEY,
    coin_family     VARCHAR(100),
    weight          VARCHAR(50),
    best_price      NUMERIC(12, 2),
    best_price_per_oz NUMERIC(12, 2),
    dealer          VARCHAR(100),
    product_name_clean VARCHAR(500),
    year            VARCHAR(10),
    currency        VARCHAR(10),
    listing_url     TEXT
);