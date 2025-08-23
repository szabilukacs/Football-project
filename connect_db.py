from sqlalchemy import MetaData, create_engine

# --- PostgreSQL kapcsolat beállítása ---
db_user = "postgres"
db_pass = "robinson00POST"
db_host = "localhost"
db_port = "5432"
db_name = "Football_stats"

# SQLAlchemy engine létrehozása
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

metadata = MetaData()
