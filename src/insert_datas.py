import pandas as pd
from .connect_db import engine
from .clean_data import validate_data_column_names, drop_null_values, validate_values, clean_and_validate

def load_teams(df: pd.DataFrame) -> pd.DataFrame:
    
    # Home and Away teams rename
    home_teams = df[['home_team']].rename(columns={'home_team': 'team_name'})
    away_teams = df[['away_team']].rename(columns={'away_team': 'team_name'})

    # Concat and drop duplicates
    df_teams = pd.concat([home_teams, away_teams]).drop_duplicates()

    # Insert it to database
    df_teams.to_sql('teams', engine, if_exists='append', index=False)

def load_matches(df: pd.DataFrame) -> pd.DataFrame:
    # Meccsek
    df_matches = df[['match_date','home_team_id','away_team_id','ft_home_goals','ft_away_goals','ft_result','ht_home_goals','ht_away_goals','ht_result','home_elo','away_elo','home_form3','home_form5','away_form3','away_form5','home_shots','away_shots',
                     'home_target','away_target','home_fouls','away_fouls','home_corners','away_corners','home_yellow','away_yellow','home_red','away_red','division_name']]

    # --- Matches tábla feltöltése ---
    df_matches.to_sql('matches', engine, if_exists='append', index=False,chunksize=5000)