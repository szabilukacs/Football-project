import pandas as pd
from sqlalchemy import create_engine

# --- PostgreSQL kapcsolat beállítása ---
db_user = "postgres"
db_pass = "robinson00POST"
db_host = "localhost"
db_port = "5432"
db_name = "Football_stats"

# SQLAlchemy engine létrehozása
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")


# CSV beolvasása
matches_df = pd.read_csv("test_data.csv")

# Feltételezzük, hogy a teams DataFrame így néz ki:
# teams_df = pd.DataFrame({'id':[1,2,3,4], 'team_name':['Marseille','Troyes','Paris SG','Strasbourg']})
teams_df = pd.read_sql_table('teams',engine)

# Csapatnév -> id mapping készítése
team_mapping = dict(zip(teams_df['team_name'], teams_df['team_id']))

matches_df = matches_df.rename(columns={"HomeTeam": "home_team_id","AwayTeam": "away_team_id"})
# HomeTeam és AwayTeam cseréje id-ra
matches_df['home_team_id'] = matches_df['home_team_id'].map(team_mapping)
matches_df['away_team_id'] = matches_df['away_team_id'].map(team_mapping)

# Eredmény mentése új CSV-be
matches_df.to_csv("test_data_ids.csv", index=False)

print("Csapatnevek cserélve ID-kra, új CSV létrehozva: matches_with_ids.csv")
