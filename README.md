# GOAT Sneaker Data Crawler

> A distributed, high-concurrency sneaker data collection system built with Python. Covers SKU scraping from Nike China and product price details from GOAT, featuring a Redis distributed queue + MySQL persistent storage architecture.

## Project Overview

This project is a data collection system for the sneaker secondary market, consisting of two independent modules that work together:

1. **Nike SKU Collection Module** (`nike_sku_redis`): Scrapes men's shoe SKUs in bulk from the Nike China product wall API, deduplicates automatically via a Redis Set, and uses it as the data source.
2. **GOAT Product Detail Collection Module** (`goat_shoes_data_mysql`): Consumes the SKU queue from Redis, maps each SKU to a `template_id` via the GOAT search API, then fetches per-size lowest prices from the product variants endpoint, and finally persists everything to MySQL.

The two modules are decoupled through Redis and can be deployed and scaled independently.

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.10 |
| HTTP Client | `requests`, `curl_cffi` (TLS fingerprint impersonation) |
| Concurrency | `multiprocessing` (multi-process) + `concurrent.futures` (thread pool) |
| Distributed Queue / Deduplication | Redis (Set, atomic SPOP) |
| Storage | MySQL (`pymysql`) |
| Logging | `logging` (console + file dual output) |

## System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Nike官网 API    │────▶│  nike_sku_redis   │────▶│  Redis Set (sku)    │
│  Product Wall    │     │  4-process crawl  │     │  Auto-dedup / Queue  │
└─────────────────┘     └──────────────────┘     └─────────┬───────────┘
                                                           │ Atomic SPOP
                                                           ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  MySQL Database  │◀────│ goat_shoes_data  │◀────│  GOAT Search/Variant │
│  goat_goods table│     │ 7 proc + 6 threads│     │  template_id mapping │
└─────────────────┘     └──────────────────┘     └─────────────────────┘
```

## Core Modules

### 1. nike_sku_redis — Nike SKU Collection

- **Entry**: `main.py` → `core/service.py` → `core/handler.py`
- **Concurrency Strategy**: 4 processes, each assigned URL groups by modulo (10 URLs per group) to avoid duplicate scraping
- **Request Method**: `requests.Session` connection reuse, random delay (2~5s) to reduce ban risk
- **Data Processing**: Parse `productGroupings` → `products` → `productCode` to extract SKUs
- **Storage**: `SADD` into Redis Set, automatic deduplication via set semantics

### 2. goat_shoes_data_mysql — GOAT Product Detail Collection

- **Entry**: `main.py` → `core/service.py` → `core/handler.py`
- **Concurrency Strategy**: Hybrid 7-process × 6-thread architecture
  - Process layer: Each process atomically pops SKUs from Redis via `SPOP` until the queue is empty
  - Thread layer: Within each process, constructed request params are evenly distributed to 6 threads for concurrent requests
- **Anti-crawl**: `curl_cffi` impersonates Chrome 124 TLS fingerprint to bypass Cloudflare protection
- **Data Flow**:
  1. `SPOP` a SKU from Redis
  2. Call GOAT search endpoint `get-product-search-results` to get `template_id`
  3. Call product variants endpoint `product_variants/buy_bar_data` to get per-size lowest price (`lowestPriceCents`)
  4. Parse fields: SKU, size, price
  5. Batch insert into MySQL `goat_goods` table

## Technical Highlights

1. **Redis Distributed Task Queue**: Atomic `SPOP` enables safe multi-process consumption with native horizontal scaling — adding more processes requires no changes to allocation logic
2. **Redis Set Deduplication**: The Nike collector uses `SADD` for automatic deduplication, ensuring downstream SKU uniqueness
3. **Hybrid Multi-process + Multi-thread Concurrency**: IO-bound tasks run concurrently at the thread layer, while CPU/network overhead is isolated at the process layer — balancing efficiency and stability
4. **TLS Fingerprint Impersonation**: `curl_cffi` mimics browser TLS handshake characteristics to defeat Cloudflare JA3 fingerprint detection
5. **Session Connection Reuse**: Each thread reuses the same `Session`, reducing TCP handshake overhead
6. **Layered Architecture**: `config / core / dao / utils` four-layer separation with clear responsibilities for configuration, business logic, data access, and utilities
7. **Exception Isolation**: A single SKU parsing failure does not break the overall flow — `try/except` skips and continues

## Project Structure

```
.
├── nike_sku_redis/                  # Nike SKU collection module
│   ├── main.py                      # Program entry
│   ├── config/                      # Configuration layer
│   │   ├── settings.py              # Process count & global config
│   │   ├── url_settings.py          # Request URL / Headers / Cookies
│   │   └── logging_settings.py      # Logging config
│   ├── core/                        # Core business layer
│   │   ├── service.py               # Multi-process scheduling
│   │   └── handler.py               # Request sending & data parsing
│   ├── dao/                         # Data access layer
│   │   └── save_data.py             # Redis write operations
│   └── utils/                       # Utility layer
│       ├── logger.py                # Logging utility
│       └── utils.py                 # URL generation utility
│
├── goat_shoes_data_mysql/           # GOAT product detail collection module
│   ├── main.py                      # Program entry
│   ├── config/                      # Configuration layer
│   │   ├── settings.py              # Process count config
│   │   ├── url_settings.py          # Variant endpoint config
│   │   ├── url_template_id_settings.py  # Search endpoint config
│   │   └── logging_settings.py      # Logging config
│   ├── core/                        # Core business layer
│   │   ├── service.py               # Multi-process scheduling
│   │   └── handler.py               # SKU→template_id mapping, data parsing
│   ├── dao/                         # Data access layer
│   │   ├── data_base.py             # Redis connection
│   │   └── save_data.py             # MySQL write operations
│   └── utils/                       # Utility layer
│       ├── logger.py                # Logging utility
│       └── utils.py                 # Multi-thread batch request utility
│
├── goat球鞋数据.py                   # Standalone GOAT data collection script
├── nike男鞋所有货号.py                # Standalone Nike SKU collection script
├── product_template_id.py           # Standalone GOAT template_id fetch script
└── README.md
```

## Requirements

- Python 3.10+
- Redis 6.0+ (password required, default db=2)
- MySQL 5.7+ / 8.0+
- Dependencies:

```bash
pip install requests curl_cffi redis pymysql
```

## Database Setup

```sql
CREATE DATABASE text3 DEFAULT CHARACTER SET utf8mb4;

CREATE TABLE goat_goods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    商品货号 VARCHAR(64),
    商品尺寸 VARCHAR(32),
    商品价格 DECIMAL(10, 2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Usage

### Step 1: Start Nike SKU Collection

```bash
cd nike_sku_redis
python main.py
```

Nike men's shoe SKUs will be automatically deduplicated and stored in the Redis `sku` set.

### Step 2: Start GOAT Product Detail Collection

```bash
cd goat_shoes_data_mysql
python main.py
```

The program consumes SKUs from Redis, scrapes price data, and writes to MySQL. It exits automatically when the Redis queue is empty.

> Note: Both modules can run simultaneously — the GOAT module will consume new SKUs written by the Nike module in real time.

## Configuration

Modify files under each module's `config/` directory:

- `settings.py`: Adjust process count (`PROCESS_NUM`)
- `url_settings.py`: Update Cookies, Headers (GOAT's `cf_clearance`, `x-csrf-token`, etc. need periodic refresh)
- `dao/save_data.py` / `dao/data_base.py`: Modify Redis and MySQL connection info (host, password, database)

## Disclaimer

This project is intended solely for learning and researching Python web scraping techniques. Do not use it for large-scale commercial data collection. Please comply with the target websites' `robots.txt` policies and relevant laws and regulations, control request frequency reasonably, and avoid causing stress on target servers.
