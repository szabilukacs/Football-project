import pandas as pd
from .connect_db import engine

def change_team_names_to_ids():
    # CSV beolvasása
    matches_df = pd.read_csv("Data/Matches.csv")

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
    matches_df.to_csv("Data/Matches_with_id.csv", index=False)

    print("Csapatnevek cserélve ID-kra, új CSV létrehozva: matches_with_ids.csv")
