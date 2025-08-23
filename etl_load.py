import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine

# --- PostgreSQL kapcsolat beállítása ---
db_user = "postgres"
db_pass = "robinson00POST"
db_host = "localhost"
db_port = "5432"
db_name = "Football_stats"

# SQLAlchemy engine létrehozása
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

metadata = MetaData()

# --- Tábla definíciók SQLAlchemy-vel ---
divisions = Table(
    'divisions', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('division_name', String, unique=True)
)

teams = Table(
    'teams', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('team_name', String),
    Column('division_id', Integer, ForeignKey('divisions.id'))
)

# --- CSV beolvasása pandas-szal ---
csv_file = "test_data.csv"  #  le kell menteni igazi csv comma delimited versionbe
df = pd.read_csv(csv_file,encoding='utf-8',sep=',')

# --- Oszlopok javítása és név tisztítása ---
df.columns = df.columns.str.strip()  # törli a felesleges szóközöket

# --- DataFrame-ek létrehozása ---
df_table2 = df[['division_name']].drop_duplicates()  # divisions tábla, ismétlődések nélkül

# --- Divisions tábla feltöltése ---
df_table2.to_sql('divisions', engine, if_exists='append', index=False)

# --- Teams tábla feltöltése ---
# Reláció létrehozása: division_id-t hozzárendeljük a divisions táblából
# Lekérjük az divisions táblát, hogy megkapjuk az id-ket
divisions_df = pd.read_sql('divisions', engine)

# Merge a division_name alapján, hogy legyen division_id
df_table1 = df[['team_name', 'division_name']].merge(divisions_df, on='division_name')
df_table1 = df_table1[['team_name', 'division_id']]  # csak team_name és division_id kell
df_table1 = df_table1.rename(columns={'id': 'division_id'})

# Feltöltés a teams táblába
df_table1.to_sql('teams', engine, if_exists='append', index=False)

print("Adatok sikeresen feltöltve a divisions és teams táblákba!")