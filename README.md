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
