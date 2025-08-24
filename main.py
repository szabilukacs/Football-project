import pandas as pd
from src.insert_datas import load_teams, load_matches
from src.clean_data import clean_and_validate, change_team_names_to_ids

if __name__ == "__main__":

    # CSV files
    csv_file = "Data/Matches.csv" 
    csv_file_with_id = "Data/Matches_with_id.csv"

    # Load csv data
    df = pd.read_csv(csv_file,encoding='utf-8',sep=',')

    # Clean data
    df = clean_and_validate(df)

    # Select team names and insert into a table
    load_teams(df)
    # Change team names to ids in the csv file based on the teams table
    change_team_names_to_ids(csv_file, csv_file_with_id)
    # Load csv data
    df = pd.read_csv(csv_file_with_id,encoding='utf-8',sep=',')
    # Insert data into the matches table based on the modified csv
    load_matches(df)

    print("OK")
    