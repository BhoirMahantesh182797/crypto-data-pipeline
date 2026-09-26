import logging
import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_crypto_data():
    logging.info("Starting Crypto API Extraction")

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        'ids':'bitcoin,ethereum,dogecoin',
        'vs_currencies':'usd',
        'include_24hr_change':'true',
    }

    try:
        logging.info(f"Fetching data from: {url}")

        response = requests.get(url, params=params)

        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame.from_dict(data, orient = 'index')
        df['fetch_timestamp'] = datetime.now()

        logging.info("Data Successfully extracted and loaded into DataFrame")

        print("\n---EXTRACTED CRYPTO DATA---")
        print(df)
        print("-----------------------------\n")

        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"API Request failed: {e}")
        return None
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def load_to_postgres(df):
    logging.info("Starting database load process")

    db_url = "postgresql://admin:password123@127.0.0.1:5432/crypto_db"

    try:
        engine = create_engine(db_url)
        logging.info("Successfully connected to PostgreSQL.")

        df.to_sql(
            name = 'raw_crypto_prices',
            con = engine,
            if_exists = 'append',
            index = True
        )

        logging.info("Data successfully loaded into 'raw_crypto_prices' table in PostgreSQL.")

    except Exception as e:
        logging.error(f"Failed to load data into PostgreSQL: {e}")

if __name__ == "__main__":

    crypto_df = extract_crypto_data()

    if crypto_df is not None:
        load_to_postgres(crypto_df)