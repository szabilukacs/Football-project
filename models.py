from sqlalchemy import Table, Column, Integer, CHAR, Date, String, ForeignKey
from connect_db import metadata
# --- Tábla definíciók SQLAlchemy-vel ---
divisions = Table(
    'divisions', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('division_name', String, unique=True)
)

teams = Table(
    'teams', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('team_name', String, unique=True),
    Column('division_id', Integer, ForeignKey('divisions.id'))
)

matches = Table(
    'matches',metadata,
    Column('match_id',Integer, primary_key = True, autoincrement=True),
    Column('match_date',Date, nullable=False),
    Column('home_team_id',Integer, ForeignKey("teams.id"), nullable=False),
    Column('away_team_id',Integer, ForeignKey("teams.id"), nullable=False),
    Column('ft_home_goals',Integer),
    Column('ft_away_goals',Integer),
    Column('ft_result',CHAR(1)),
    Column('ht_home_goals',Integer),
    Column('ht_away_goals',Integer),
    Column('ht_result',CHAR(1))
)