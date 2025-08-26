"""
main.py

Entry point of the ETL pipeline:
- Reads raw match data from CSV
- Cleans and validates the data
- Inserts teams and matches into PostgreSQL
- Prevents duplicate loading if data already exists
"""

import pandas as pd
import logging

from src.insert_datas import load_teams, load_matches
from src.clean_data import clean_and_validate, change_team_names_to_ids
from src.connect_db import ensure_database_initialized
from src.connect_db import conn

# CSV files paths
CSV_RAW_PATH = "Data/Matches.csv" 
CSV_WITH_ID_PATH = "Data/Matches_with_id.csv"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    # check if database exists if not then create it
    try:
        if not ensure_database_initialized():
            logging.info("Database empty or not existing. Starting data load...")

            # Load csv data
            df = pd.read_csv(CSV_RAW_PATH,encoding='utf-8',sep=',')

            # Clean data
            df = clean_and_validate(df)

            # Insert teams into teams table
            load_teams(df)

            # Replcae team names with IDs in a new csv
            change_team_names_to_ids(CSV_RAW_PATH, CSV_WITH_ID_PATH)

            # Load new csv data file
            df = pd.read_csv(CSV_WITH_ID_PATH,encoding='utf-8',sep=',')

            # Insert matches
            load_matches(df)
            logging.info("Datas loaded inot the database succesfully!")
        else:
            logging.info("Datas already exists")
            # TODO: Add crawling for Premier League matches API
        
        conn.close()
    except Exception as e:
        logging.error("ETL process failed",exc_info=True)
    finally:
        conn.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
    