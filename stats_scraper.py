from bs4 import BeautifulSoup as bs
import requests as req
import pandas
from pandas import DataFrame

BASE_URL = "https://www.transfermarkt.co.uk"
RECORD_URL = "https://www.transfermarkt.co.uk/moises-caicedo/bilanzdetails/spieler/687626/plus//gegner/873"


def get_soup(url: str) -> bs:
    page = req.get(url,
                   headers={
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                   }
                   )
    return bs(page.text, "html.parser")


def find_pl_teams() -> list[dict]:
    """
    find premier league teams from Transfermarkt
    along with their href which includes their unique ID
    """

    url = f"{BASE_URL}/premier-league/startseite/wettbewerb/GB1"
    page = req.get(url,
                   headers={
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                   }
                   )
    print(page)
    soup = bs(page.text, "html.parser")

    box = soup.find_all("div", class_="box")
    keys = box[1].find("div", class_="keys")

    teams_list = []

    for team in keys.find_all("span"):
        decoded_soup = bs(team.text, "html.parser")
        teams_list.append(decoded_soup.find("a").attrs)

    return teams_list


def find_squad_list(team: dict) -> list[dict]:
    """
    find a list of players that play for a team from TransferMarkt
    along with their href which includes unique ID
    """

    soup = get_soup(BASE_URL + team["href"])
    players_html = soup.find_all("td", class_="posrela")
    players = []
    possible_inactive = [
        "no eligibility",
        "return expected on",
        "return unknown",
        "red card",
        "suspension"
    ]
    for player_html in players_html:
        player = player_html.find(
            "table", class_="inline-table").find("a")

        player_name = player.text
        attributes = player.attrs

        active = True

        span = player.find("span")
        if span:
            if any(inactive in span.attrs["title"].lower() for inactive in possible_inactive):
                active = False

        if active:
            """get player stats table"""
            df = DataFrame()

        players.append({
            "name": player_name.strip(),
            "href": attributes["href"],
            "active": active
        })

    return players


def display_teams(teams_list: list[dict]) -> dict[dict]:
    for i, team in enumerate(teams_list):
        print(f"{i+1}. {team["title"]}")

    print("")
    home = int(input("Pick a home team(1-20): "))
    away = int(input("Pick an away team(1-20): "))

    return {"home": teams_list[home-1], "away": teams_list[away-1]}


def extract_id(url: str) -> str:
    for page in url.split("/"):
        try:
            int(page)
            return page
        except ValueError:
            continue


def generate_record_url(player: dict, team: dict) -> str:
    url = BASE_URL + player["href"]
    url = url.replace("profil", "bilanzdetails") + \
        "/plus//gegner/" + extract_id(team["href"])

    return url


def extract_record_table(url: str) -> DataFrame:
    """extract table for players record against club"""
    soup = get_soup(url)
    table = soup.find("table")
    # print(table.prettify())
    # df = pandas.read_html(tables)
    # print(df)
    headers_list = []
    headers = table.find_all("th")
    for header in headers:
        if header.get("class") == ["hide"]:
            continue
        if header.find("span"):
            headers_list.append(header.find("span").get("title"))
        else:
            headers_list.append(header.text)

    df = DataFrame(columns=headers_list)

    row_data = table.find_all("tr")[1:]
    for row in row_data:
        data = row.find_all("td")
        row_list = [col.text for col in data if col.get("class") != [
            "hide"] and col.text]

        df.loc[len(df)] = row_list

    return df


def main():
    """main function"""
    teams_list = find_pl_teams()
    match = display_teams(teams_list)
    print(f"{match["home"]["title"]} vs. {match["away"]["title"]}")
    home_players = find_squad_list(match["home"])
    away_players = find_squad_list(match["away"])

    print(f"{match["home"]["title"]} available squad:")

    for home_player in [player for player in home_players if player["active"]]:
        print(home_player["name"])

    print(" ")
    print(home_player)
    print(" ")

    print(f"{match["away"]["title"]} available squad:")

    for away_player in [player for player in away_players if player["active"]]:
        print(away_player["name"])


def main2():
    teams_list = find_pl_teams()
    players = find_squad_list(teams_list[3])
    print(players[4])
    print(teams_list[2])
    record_url = generate_record_url(players[4], teams_list[2])
    print(record_url)
    extract_record_table(record_url)


if __name__ == "__main__":
    main2()
