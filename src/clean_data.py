
"""
clean_data.py

Data cleaning and validation utilities for football matches dataset.
- Normalizes column names
- Removes invalid or incomplete rows
- Validates values (no future matches, no negative goals)
- Maps team names to database IDs
"""

import pandas as pd
import datetime
import logging
from .connect_db import conn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def change_team_names_to_ids(csv_file: str, csv_file_out: str) -> None:
    """
    Replace team names with corresponding team IDs based on the database,
    and save the updated matches to a new CSV file.

    Args:
        csv_file (str): Path to the input CSV containing team names.
        csv_file_out (str): Path to the output CSV with team IDs.
    """

    matches_df = pd.read_csv(csv_file)
    teams_df = pd.read_sql("SELECT * FROM teams;",conn)

    # Mapping team name - team id
    team_mapping = dict(zip(teams_df['team_name'], teams_df['team_id']))

    # Rename columns
    matches_df = matches_df.rename(columns={"Home_Team": "home_team_id","Away_Team": "away_team_id"})

    # HomeTeam and AwayTeam replace to IDs
    matches_df['home_team_id'] = matches_df['home_team_id'].map(team_mapping)
    matches_df['away_team_id'] = matches_df['away_team_id'].map(team_mapping)

    # Check for unmapped teams
    if matches_df["home_team_id"].isnull().any() or matches_df["away_team_id"].isnull().any():
        logging.warning("Some team names could not be mapped to IDs.")

    # Eredmény mentése új CSV-be
    matches_df.to_csv(csv_file_out, index=False)

    logging.info(f"File {csv_file_out} created successfully.")


def validate_data_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names: lowercase, strip spaces, replace spaces with underscores.
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

def drop_null_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows with null values in mandatory columns.
    """
    df = df.dropna(subset=['match_date', 'home_team', 'away_team',
                           'ft_home_goals','ft_away_goals','ft_result'])

    return df

def validate_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate dataset values:
    - Remove negative goal counts
    - Remove matches with future dates
    """
    today = datetime.date.today()

    # Remove negative goals
    df = df[(df['ft_home_goals'] >= 0) & (df['ft_away_goals'] >= 0)]

    # Remove future matches
    df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')
    df = df[df['match_date'].dt.date <= today]

    return df

def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate a matches DataFrame.
    Steps:
    1. Normalize column names
    2. Drop rows with null values
    3. Validate logical consistency of data
    """

    df = validate_data_column_names(df)
    df = drop_null_values(df)
    df = validate_values(df)

    logging.info("Values validated successfully.")

    return df