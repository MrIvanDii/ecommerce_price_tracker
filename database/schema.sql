-- Gold Price Tracker — Database Schema
-- Run once to initialize tables

USE gold_tracker;

-- Current prices (truncated and reloaded on every scraper run)
CREATE TABLE IF NOT EXISTS price_latest (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp VARCHAR(50),
    dealer VARCHAR(100),
    product_name_clean VARCHAR(255),
    coin_family VARCHAR(100),
    year VARCHAR(10),
    weight VARCHAR(20),
    price DECIMAL(10,2),
    price_per_oz DECIMAL(10,2),
    currency VARCHAR(10),
    availability VARCHAR(50),
    listing_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rolling 90-day history (appended on every run, old records deleted)
CREATE TABLE IF NOT EXISTS price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp VARCHAR(50),
    dealer VARCHAR(100),
    product_name_clean VARCHAR(255),
    coin_family VARCHAR(100),
    year VARCHAR(10),
    weight VARCHAR(20),
    price DECIMAL(10,2),
    price_per_oz DECIMAL(10,2),
    currency VARCHAR(10),
    availability VARCHAR(50),
    listing_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Best price per coin group (truncated and reloaded on every scraper run)
CREATE TABLE IF NOT EXISTS price_best (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_family VARCHAR(100),
    weight VARCHAR(20),
    best_price DECIMAL(10,2),
    best_price_per_oz DECIMAL(10,2),
    dealer VARCHAR(100),
    product_name_clean VARCHAR(255),
    year VARCHAR(10),
    currency VARCHAR(10),
    listing_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);