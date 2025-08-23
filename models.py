from sqlalchemy import Table, Column, Integer, CHAR, Date, String, ForeignKey
from connect_db import metadata
# --- Tábla definíciók SQLAlchemy-vel ---
divisions = Table(
    'divisions', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
)

teams = Table(
    'teams', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('team_name', String, unique=True),
    Column('division_id', Integer, ForeignKey('divisions.id'))
)

matches = Table(
    'matches',metadata,
    Column('division_name',CHAR(4)),
    Column('match_id',Integer, primary_key = True, autoincrement=True),
    Column('match_date',Date, nullable=False),
    Column('home_team_id',Integer, ForeignKey("teams.id"), nullable=False),
    Column('away_team_id',Integer, ForeignKey("teams.id"), nullable=False),
    Column('home_elo',float),
    Column('away_elo',float),
    Column('home_form3',Integer),
    Column('home_form5',Integer),
    Column('away_form3',Integer),
    Column('away_form5',Integer),
    Column('ft_home_goals',Integer),
    Column('ft_away_goals',Integer),
    Column('ft_result',CHAR(1)),
    Column('ht_home_goals',Integer),
    Column('ht_away_goals',Integer),
    Column('ht_result',CHAR(1)),
    Column('home_shots',Integer),
    Column('away_shots',Integer),
    Column('home_target',Integer),
    Column('away_target',Integer),
    Column('home_fouls',Integer),
    Column('away_fouls',Integer),
    Column('home_corners',Integer),
    Column('away_corners',Integer),
    Column('home_yellow',Integer),
    Column('away_yellow',Integer),
    Column('home_red',Integer),
    Column('away_red',Integer),
)

match_stats = Table(
    'match_stats',metadata,
    Column('stat_id',Integer, primary_key = True, autoincrement=True),
    Column('match_id',Integer, ForeignKey("matches.match_id"), nullable=False),

)