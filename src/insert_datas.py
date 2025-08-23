import pandas as pd
from .connect_db import engine

def load_div_and_teams():
    # --- CSV beolvasása pandas-szal ---
    csv_file = "Data/Matches.csv"  #  le kell menteni hogy igazi csv comma delimited versionbe
    df = pd.read_csv(csv_file,encoding='utf-8',sep=',')

    # --- Oszlopok javítása és név tisztítása ---
    df.columns = df.columns.str.strip()  # törli a felesleges szóközöket

    # Home és Away csapatok összegyűjtése
    home_teams = df[['HomeTeam']].rename(columns={'HomeTeam': 'team_name'})
    away_teams = df[['AwayTeam']].rename(columns={'AwayTeam': 'team_name'})

    # Egyesítés és duplikátumok eltávolítása
    df_teams = pd.concat([home_teams, away_teams]).drop_duplicates()

    # Feltöltés a teams táblába
    df_teams.to_sql('teams', engine, if_exists='append', index=False,chunksize=10000)

def load_matches():
    # --- CSV beolvasása pandas-szal ---
    csv_file = "Data/Matches_with_id.csv"  #  le kell menteni igazi csv comma delimited versionbe
    df = pd.read_csv(csv_file,encoding='utf-8',sep=',')

    # --- Oszlopok javítása és név tisztítása ---
    df.columns = df.columns.str.strip()  # törli a felesleges szóközöket

    # Meccsek
    df_matches = df[['match_date','home_team_id','away_team_id','ft_home_goals','ft_away_goals','ft_result','ht_home_goals','ht_away_goals','ht_result','home_elo','away_elo','home_form3','home_form5','away_form3','away_form5','home_shots','away_shots',
                     'home_target','away_target','home_fouls','away_fouls','home_corners','away_corners','home_yellow','away_yellow','home_red','away_red','division_name']]

    # --- Matches tábla feltöltése ---
    df_matches.to_sql('matches', engine, if_exists='append', index=False)