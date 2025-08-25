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

conn = psycopg2.connect(
    database=db_name, user=db_user, 
    password=db_pass, host=db_host, port='5432')

create_tables_path = "PostgreSQL/Create_tables.sql"

def check_database_if_has_data():

    

    cursor = conn.cursor()
    conn.autocommit = True

    # Ellenőrizzük, hogy léteznek-e a táblák
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    tables = {row[0] for row in cursor.fetchall()}

    expected_tables = {"teams", "matches"}
    has_data = True

    if tables == expected_tables:
    # Ellenőrizzük, van-e adat a táblákban
        for table in tables:
            cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
            result = cursor.fetchone()
            if not result:
                has_data = False
                break
    else:
        # Ha hiányoznak a táblák, létrehozzuk őket
        
        with open(create_tables_path, "r") as f:
            cursor.execute(f.read())
        has_data = False

    cursor.close()

    return has_data