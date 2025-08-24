from sqlalchemy import MetaData, create_engine, inspect, text
import os
from dotenv import load_dotenv
import psycopg2
# --- PostgreSQL kapcsolat beállítása ---
load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

create_tables_path = "PostgreSQL/Create_tables.sql"

# SQLAlchemy engine létrehozása
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

metadata = MetaData()

def check_database_if_has_data():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    query = ""
    has_data = True
    expected_tables = {"teams", "matches"}

    conn = psycopg2.connect(
    database="Football_stats", user='postgres', 
    password='robinson00POST', host='localhost', port='5432')

    if set(tables) == expected_tables:
        # We are loading the csv only if we  dont have tables or they are ures
        if tables:
            with engine.connect() as conn:
                for table in tables:
                    result = conn.execute(text(f"SELECT 1 FROM {table} LIMIT 1")).first()
                    if not result:
                        has_data = False
                        break
    # We are creating the tables
    else:
        conn.autocommit = True
        cursor = conn.cursor()

        with open(create_tables_path) as f:
            cursor.execute(f.read())

        conn.commit()
        conn.close()
        has_data = False

    return has_data