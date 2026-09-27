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

🛠️ Tech Stack
Extraction & Orchestration: Python 3.9+, requests, pandas, Prefect
Storage: PostgreSQL 15 (Containerized via Docker)
Transformation & Testing: dbt-core, dbt-postgres
Version Control: Git & GitHub

📂 Project Structure
crypto-pipeline/
├── .venv/                  # Python virtual environment (ignored)
├── src/
│   ├── ingestion/
│   │   └── extract_crypto.py    # Python script to fetch API data & load to Postgres
│   └── orchestration/
│       └── run_pipeline.py      # Prefect flow orchestrating the entire pipeline
├── crypto_transform/       # dbt project directory
│   ├── dbt_project.yml
│   ├── profiles.yml        # Database connection config
│   └── models/
│       ├── staging/
│       │   ├── sources.yml       # Defines external raw tables + data quality tests
│       │   └── stg_crypto_prices.sql # SQL transformation model
├── .gitignore
├── requirements.txt
└── README.md

🚀 How to Run Locally

1. Prerequisites
Install Docker Desktop and ensure it is running.
Have Python 3.9+ installed.

2. Setup the Database
Spin up a local PostgreSQL container:
docker run --name crypto-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=password123 \
  -e POSTGRES_DB=crypto_db \
  -p 5432:5432 \
  -d postgres:15

  4. Setup dbt
  # Install dbt postgres adapter
pip install dbt-postgres

# Verify connection to the Docker database
cd crypto_transform
dbt debug
cd ..

5. Run the Orchestrated Pipeline
Execute the entire pipeline (Extract → Load → Transform → Test) in one command:
python src/orchestration/run_pipeline.py

🔍 Data Quality
This pipeline enforces strict data quality gates using dbt tests. Before any data is considered "ready", dbt automatically verifies:
not_null on the usd price column.
not_null on the fetch_timestamp audit column.
If any of these tests fail, the Prefect orchestration flow will halt, preventing bad data from propagating downstream.

🚀 Future Enhancements
Cloud Deployment: Migrate the local PostgreSQL database to AWS RDS or GCP Cloud SQL, and run the Prefect agent on an EC2 instance or Kubernetes cluster.
Incremental Models: Update the dbt stg_crypto_prices model to use materialized='incremental' to only process new records, reducing compute costs at scale.
CI/CD Integration: Add GitHub Actions to automatically run dbt test and dbt run on every pull request to the main branch.
