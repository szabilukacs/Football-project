from get_team_ids import change_team_names_to_ids
from insert_datas import load_div_and_teams, load_matches

if __name__ == "__main__":

    load_div_and_teams()

    change_team_names_to_ids()

    load_matches()

    print("OK")
    