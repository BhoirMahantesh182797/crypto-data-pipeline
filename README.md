# 🚀 Crypto Data Pipeline (Modern Data Stack)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![dbt](https://img.shields.io/badge/dbt-Core-FF694B.svg)](https://www.getdbt.com/)
[![Prefect](https://img.shields.io/badge/Prefect-2.10+-0D083F.svg)](https://www.prefect.io/)

An end-to-end, production-grade batch data pipeline that extracts live cryptocurrency market data, loads it into a relational database, transforms it using SQL, enforces data quality, and orchestrates the entire workflow.

## 🏗️ Architecture

This project follows modern Data Engineering best practices, separating concerns into distinct, testable layers:

```mermaid
graph LR
    A[CoinGecko API] -->|Python Requests| B(Bronze: Raw PostgreSQL)
    B -->|dbt source| C(Silver: dbt Staging Model)
    C -->|dbt test| D{Data Quality Checks}
    D -->|Prefect Flow| E[Analytics Ready]
    
    style B fill:#e1e1e1,stroke:#333
    style C fill:#add8e6,stroke:#333
    style D fill:#90ee90,stroke:#333

# 🛠️ Tech Stack
# Extraction & Orchestration: Python 3.9+, requests, pandas, Prefect
# Storage: PostgreSQL 15 (Containerized via Docker)
# Transformation & Testing: dbt-core, dbt-postgres
# Version Control: Git & GitHub

# 📂 Project Structure

crypto-pipeline/
├── .venv/
├── src/
│   ├── ingestion/
│   │   └── extract_crypto.py
│   └── orchestration/
│       └── run_pipeline.py
├── crypto_transform/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       └── staging/
│           ├── sources.yml
│           └── stg_crypto_prices.sql
├── .gitignore
├── requirements.txt
└── README.md

# 🚀 How to Run Locally
# 1. Prerequisites
# Install Docker Desktop and ensure it is running.
# Have Python 3.9+ installed.

# 2. Setup the Database
docker run --name crypto-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=password123 \
  -e POSTGRES_DB=crypto_db \
  -p 5432:5432 \
  -d postgres:15

# 3. Setup Python Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. Setup dbt
pip install dbt-postgres
cd crypto_transform
dbt debug
cd ..

# 5. Run the Orchestrated Pipeline
python src/orchestration/run_pipeline.py


# 🔍 Data Quality
# This pipeline enforces strict data quality gates using dbt tests:
# not_null on the usd price column
# not_null on the fetch_timestamp audit column
# If any test fails, the Prefect flow halts, preventing bad data from propagating downstream.

# 🔮 Future Enhancements
# Cloud Deployment: Migrate PostgreSQL to AWS RDS or GCP Cloud SQL
# Incremental Models: Use materialized='incremental' in dbt for cost efficiency
# CI/CD: Add GitHub Actions to auto-run dbt test on every pull request
# EOF
