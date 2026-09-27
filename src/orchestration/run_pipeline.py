import logging
import subprocess
import sys
from pathlib import Path
from prefect import flow, task

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 🧠 SENIOR DE TRICK: Dynamically find the project root using the file's own location!
PROJECT_ROOT = Path(__file__).parent.parent.parent
DBT_PROJECT_DIR = PROJECT_ROOT / "crypto_transform"
EXTRACTION_SCRIPT = PROJECT_ROOT / "src" / "ingestion" / "extract_crypto.py"

PYTHON_EXEC = sys.executable

@task(name="Extract Crypto Data")
def extract_data():
    logging.info(f"Running extraction script at: {EXTRACTION_SCRIPT}")
    result = subprocess.run(
        [PYTHON_EXEC, str(EXTRACTION_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT)
    )
    print(result.stdout)
    if result.returncode != 0:
        logging.error(f"Extraction failed:\n{result.stderr}")
        raise Exception("Extraction task failed")
    logging.info("Extraction completed successfully!")

@task(name="Transform with dbt")
def transform_data():
    logging.info("Running dbt run...")
    result = subprocess.run(
        ["dbt", "run"],
        capture_output=True,
        text=True,
        cwd=str(DBT_PROJECT_DIR)
    )
    print(result.stdout)
    if result.returncode != 0:
        logging.error(f"dbt run failed:\n{result.stderr}")
        raise Exception("dbt run task failed")
    logging.info("dbt run completed successfully!")

@task(name="Test Data Quality with dbt")
def test_data():
    logging.info("Running dbt test...")
    result = subprocess.run(
        ["dbt", "test"],
        capture_output=True,
        text=True,
        cwd=str(DBT_PROJECT_DIR)
    )
    print(result.stdout)
    if result.returncode != 0:
        logging.error(f"dbt test failed:\n{result.stderr}")
        raise Exception("dbt test task failed")
    logging.info("All data quality tests passed!")

@flow(name="Crypto Data Pipeline")
def crypto_pipeline_flow():
    logging.info("🚀 Starting Crypto Data Pipeline Flow...")
    extract_data()
    transform_data()
    test_data()
    logging.info("✅ Pipeline Flow completed successfully!")

if __name__ == "__main__":
    crypto_pipeline_flow()