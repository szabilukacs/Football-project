"""
load_data.py

ETL Load step:
- Insert unique teams into the `teams` table
- Insert matches into the `matches` table
"""
import logging
import pandas as pd
from src.connect_db import conn
from psycopg2.extras import execute_values

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_teams(df: pd.DataFrame) -> None:
    """
    Load unique teams into the `teams` table.

    Args:
        df (pd.DataFrame): DataFrame containing `home_team` and `away_team` columns.
    """

    # Home and Away teams rename
    home_teams = df[['home_team']].rename(columns={'home_team': 'team_name'})
    away_teams = df[['away_team']].rename(columns={'away_team': 'team_name'})

    # Concat and drop duplicates
    df_teams = pd.concat([home_teams, away_teams]).drop_duplicates()

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO teams (team_name)
        VALUES %s
        ON CONFLICT (team_name) DO NOTHING;
    """

    team_values = [(team,) for team in df_teams["team_name"]]

    try:
        execute_values(cursor, insert_query, team_values)
        conn.commit()
        logging.info(f"Inserted {len(team_values)} teams into `teams` table.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting teams: {e}")
        raise
    finally:
        cursor.close()

def load_matches(df: pd.DataFrame) -> None:
    """
    Load match data into the `matches` table.

    Args:
        df (pd.DataFrame): DataFrame containing all required match columns.
    """
    cursor = conn.cursor()

    # Ensure correct column order
    df_matches = df[[
        'division_name', 'match_date', 'home_team_id', 'away_team_id',
        'home_elo', 'away_elo', 'home_form3', 'home_form5', 'away_form3', 'away_form5',
        'ft_home_goals', 'ft_away_goals', 'ft_result', 'ht_home_goals', 'ht_away_goals',
        'ht_result', 'home_shots', 'away_shots', 'home_target', 'away_target',
        'home_fouls', 'away_fouls', 'home_corners', 'away_corners',
        'home_yellow', 'away_yellow', 'home_red', 'away_red'
    ]]

    # Pandas -> Python típusok
    values = [tuple(x) 
              for x in df_matches.astype(object).where(pd.notnull(df_matches), None).to_numpy()]

    insert_query = """
        INSERT INTO matches (
            division_name, match_date, home_team_id, away_team_id,
            home_elo, away_elo, home_form3, home_form5, away_form3, away_form5,
            ft_home_goals, ft_away_goals, ft_result, ht_home_goals, ht_away_goals,
            ht_result, home_shots, away_shots, home_target, away_target,
            home_fouls, away_fouls, home_corners, away_corners,
            home_yellow, away_yellow, home_red, away_red
        )
        VALUES %s
    """

    try:
        execute_values(cursor, insert_query, values)
        conn.commit()
        logging.info(f"Inserted {len(values)} matches into `matches` table.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting matches: {e}")
        raise
    finally:
        cursor.close()

def create_views(conn, sql_file="PostgreSQL/create_views.sql"):
    try:
        cursor = conn.cursor()
        with open(sql_file, "r", encoding="utf-8") as f:
            sql = f.read()

        # Ez futtatja az egész fájlt egyszerre
        cursor.execute(sql)

        conn.commit()
        logging.info("✅ Views created successfully.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating views: {e}", exc_info=True)
        raise
    finally:
        cursor.close()
