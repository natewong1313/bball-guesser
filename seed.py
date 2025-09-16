# python script to get players & teams and upload to database
# TODO: right now this using nba_api but the data is a little out of date
import datetime
import sys
import time
from nba_api.stats.static.teams import get_teams
from nba_api.stats.endpoints import commonteamroster
import psycopg
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise Exception("Missing DATABASE_URL")
NBA_SEASON = 2026
# this doesnt change
NBA_TEAMS = {
    "Atlanta Hawks": {
        "division": "Southeast",
        "conference": "Eastern",
    },
    "Boston Celtics": {
        "division": "Atlantic",
        "conference": "Eastern",
    },
    "Brooklyn Nets": {
        "division": "Atlantic",
        "conference": "Eastern",
    },
    "Charlotte Hornets": {
        "division": "Southeast",
        "conference": "Eastern",
    },
    "Chicago Bulls": {
        "division": "Central",
        "conference": "Eastern",
    },
    "Cleveland Cavaliers": {
        "division": "Central",
        "conference": "Eastern",
    },
    "Dallas Mavericks": {
        "division": "Southwest",
        "conference": "Western",
    },
    "Denver Nuggets": {
        "division": "Northwest",
        "conference": "Western",
    },
    "Detroit Pistons": {
        "division": "Central",
        "conference": "Eastern",
    },
    "Golden State Warriors": {
        "division": "Pacific",
        "conference": "Western",
    },
    "Houston Rockets": {
        "division": "Southwest",
        "conference": "Western",
    },
    "Indiana Pacers": {
        "division": "Central",
        "conference": "Eastern",
    },
    "Los Angeles Clippers": {
        "division": "Pacific",
        "conference": "Western",
    },
    "Los Angeles Lakers": {
        "division": "Pacific",
        "conference": "Western",
    },
    "Memphis Grizzlies": {
        "division": "Southwest",
        "conference": "Western",
    },
    "Miami Heat": {
        "division": "Southeast",
        "conference": "Eastern",
    },
    "Milwaukee Bucks": {
        "division": "Central",
        "conference": "Eastern",
    },
    "Minnesota Timberwolves": {
        "division": "Northwest",
        "conference": "Western",
    },
    "New Orleans Pelicans": {
        "division": "Southwest",
        "conference": "Western",
    },
    "New York Knicks": {
        "division": "Atlantic",
        "conference": "Eastern",
    },
    "Oklahoma City Thunder": {
        "division": "Northwest",
        "conference": "Western",
    },
    "Orlando Magic": {
        "division": "Southeast",
        "conference": "Eastern",
    },
    "Philadelphia 76ers": {
        "division": "Atlantic",
        "conference": "Eastern",
    },
    "Phoenix Suns": {
        "division": "Pacific",
        "conference": "Western",
    },
    "Portland Trail Blazers": {
        "division": "Northwest",
        "conference": "Western",
    },
    "Sacramento Kings": {
        "division": "Pacific",
        "conference": "Western",
    },
    "San Antonio Spurs": {
        "division": "Southwest",
        "conference": "Western",
    },
    "Toronto Raptors": {
        "division": "Atlantic",
        "conference": "Eastern",
    },
    "Utah Jazz": {
        "division": "Northwest",
        "conference": "Western",
    },
    "Washington Wizards": {
        "division": "Southeast",
        "conference": "Eastern",
    },
}


INSERT_TEAM_QUERY = "INSERT INTO teams (name, conference, division, logo_url, inserted_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING"


def insert_teams():
    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()

    team_data = []
    for team in get_teams():
        team_name = team["full_name"]
        team_data.append((team_name, team["id"]))
        print("Inserting", team_name)
        cur.execute(
            INSERT_TEAM_QUERY,
            (
                team_name,
                NBA_TEAMS[team_name]["conference"],
                NBA_TEAMS[team_name]["division"],
                "",
                datetime.datetime.now(),
                datetime.datetime.now(),
            ),
        )
    conn.commit()
    cur.close()
    conn.close()
    return team_data


DELETE_PLAYERS_QUERY = "DELETE FROM players WHERE team_name = %s"
INSERT_PLAYERS_QUERY = "INSERT INTO players (name, positions, age, height, number, image_url, school, team_name, inserted_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING"


def insert_players_for_team(team_name, team_id):
    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()
    print("Getting players for team", team_name)

    cur.execute(DELETE_PLAYERS_QUERY, (team_name,))

    roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_dict()
    results = roster["resultSets"]
    print(results)
    for result in results:
        if result["name"] != "CommonTeamRoster":
            continue
        for player in result["rowSet"]:
            player_name = player[3]
            player_img = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player[14]}.png?111"
            player_num = player[6]
            if player_num == "":
                continue
            player_positions = player[7].split("-")
            player_height = 0
            if "-" in player[8]:
                dimensions = player[8].split("-")
                player_height = int(dimensions[0]) * 12 + int(dimensions[1])
            else:
                player_height = player[8]
            player_age = player[11]
            player_school = player[13]
            print("Player", player_name)
            cur.execute(
                INSERT_PLAYERS_QUERY,
                (
                    player_name,
                    player_positions,
                    player_age,
                    player_height,
                    player_num,
                    player_img,
                    player_school,
                    team_name,
                    datetime.datetime.now(),
                    datetime.datetime.now(),
                ),
            )
    conn.commit()
    cur.close()
    conn.close()

    time.sleep(4)


if __name__ == "__main__":
    team_names = insert_teams()
    for team_name, team_id in team_names:
        insert_players_for_team(team_name, team_id)
