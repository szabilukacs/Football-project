
import pandas as pd
import datetime
from .connect_db import conn

def change_team_names_to_ids(csv_file: str, csv_file_out: str):
    # CSV beolvasása
    matches_df = pd.read_csv(csv_file)

    teams_df = pd.read_sql("SELECT * FROM teams;",conn)

    # Csapatnév -> id mapping készítése
    team_mapping = dict(zip(teams_df['team_name'], teams_df['team_id']))

    matches_df = matches_df.rename(columns={"Home_Team": "home_team_id","Away_Team": "away_team_id"})
    # HomeTeam és AwayTeam cseréje id-ra
    matches_df['home_team_id'] = matches_df['home_team_id'].map(team_mapping)
    matches_df['away_team_id'] = matches_df['away_team_id'].map(team_mapping)

    # Eredmény mentése új CSV-be
    matches_df.to_csv(csv_file_out, index=False)

    print("File " + csv_file_out + " created succesfully!")


def validate_data_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

def drop_null_values(df: pd.DataFrame) -> pd.DataFrame:
    # These values are mandatory
    df = df.dropna(subset=['match_date', 'home_team', 'away_team','ft_home_goals','ft_away_goals','ft_result'])

    return df

def validate_values(df: pd.DataFrame) -> pd.DataFrame:
    
    today = datetime.date.today()

    # Remove negative goals
    df = df[(df['ft_home_goals'] >= 0) & (df['ft_away_goals'] >= 0)]

    # Remove future matches
    df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')
    df = df[df['match_date'].dt.date <= today]

    return df

def clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:

    df = validate_data_column_names(df)
    df = drop_null_values(df)
    df = validate_values(df)

    print("Values validated succesfully!")

    return df