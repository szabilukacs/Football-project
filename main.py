import pandas as pd
from src.insert_datas import load_teams, load_matches
from src.clean_data import clean_and_validate, change_team_names_to_ids
from src.connect_db import check_database_if_has_data

if __name__ == "__main__":

    # CSV files
    csv_file_path = "Data/Matches.csv" 
    csv_file_with_id_path = "Data/Matches_with_id.csv"
    create_tables_path = "PostgreSQL/Create_tables.sql"

    # kijavitani ha nincsenek adatok automatikusan letrehozza a tablakat s megy tovabb
    # atterni sql alchemyrol psycog2
    if not check_database_if_has_data():

        # Load csv data
        df = pd.read_csv(csv_file_path,encoding='utf-8',sep=',')

        # Clean data
        df = clean_and_validate(df)

        # Select team names and insert into a table
        load_teams(df)
        # Change team names to ids in the csv file based on the teams table
        change_team_names_to_ids(csv_file_path, csv_file_with_id_path)
        # Load csv data
        df = pd.read_csv(csv_file_with_id_path,encoding='utf-8',sep=',')
        # Insert data into the matches table based on the modified csv
        load_matches(df)

        print("OK")
    else:
        print("Datas already there")
        # todo: itt csinalni a crawlingot tovabb akkor
    