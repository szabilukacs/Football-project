from sqlalchemy import MetaData, create_engine
import os
from dotenv import load_dotenv, dotenv_values

# --- PostgreSQL kapcsolat beállítása ---
load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# SQLAlchemy engine létrehozása
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

metadata = MetaData()
