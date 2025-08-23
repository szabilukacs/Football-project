import pandas as pd
from connect_db import engine

# --- CSV beolvasása pandas-szal ---
csv_file = "test_data.csv"  #  le kell menteni hogy igazi csv comma delimited versionbe
df = pd.read_csv(csv_file,encoding='utf-8',sep=',')

# --- Oszlopok javítása és név tisztítása ---
df.columns = df.columns.str.strip()  # törli a felesleges szóközöket

# --- DataFrame-ek divisionok létrehozása ---
df_divisions = df[['division_name']].drop_duplicates()  # divisions tábla, ismétlődések nélkül

# --- Divisions tábla feltöltése ---
df_divisions.to_sql('divisions', engine, if_exists='append', index=False)

# --- Teams tábla feltöltése ---
# Reláció létrehozása: division_id-t hozzárendeljük a divisions táblából
# Lekérjük az divisions táblát, hogy megkapjuk az id-ket
divisions_df = pd.read_sql('divisions', engine)

# Merge a division_name alapján, hogy legyen division_id, Home team alapjan valasztja ki a csapatot a teams tablaba
# Home és Away csapatok összegyűjtése
home_teams = df[['HomeTeam', 'division_name']].rename(columns={'HomeTeam': 'team_name'})
away_teams = df[['AwayTeam', 'division_name']].rename(columns={'AwayTeam': 'team_name'})

# Egyesítés és duplikátumok eltávolítása
all_teams = pd.concat([home_teams, away_teams]).drop_duplicates()

df_teams = all_teams.merge(divisions_df, on='division_name')
df_teams = df_teams[['team_name', 'division_id']]  # csak team_name és division_id kell
df_teams = df_teams.rename(columns={'id': 'division_id'})

# Feltöltés a teams táblába
df_teams.to_sql('teams', engine, if_exists='append', index=False)

# --- CSV beolvasása pandas-szal ---
csv_file = "test_data_ids.csv"  #  le kell menteni igazi csv comma delimited versionbe
df = pd.read_csv(csv_file,encoding='utf-8',sep=',')

# --- Oszlopok javítása és név tisztítása ---
df.columns = df.columns.str.strip()  # törli a felesleges szóközöket

# Meccsek
df_matches = df[['match_date','home_team_id','away_team_id','ft_home_goals','ft_away_goals','ft_result','ht_home_goals','ht_away_goals','ht_result']]

# --- Matches tábla feltöltése ---
df_matches.to_sql('matches', engine, if_exists='append', index=False)

print("Adatok sikeresen feltöltve a táblákba!")