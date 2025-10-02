from bs4 import BeautifulSoup as bs
import requests as req
from pandas import DataFrame

BASE_URL = "https://www.transfermarkt.co.uk"


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

        players.append({
            "name": player_name.strip(),
            "href": attributes["href"],
            "active": active
        })

    for i in players:
        print(f"{i["name"]}: {i["active"]}")


def display_teams(teams_list: list[dict]) -> dict[dict]:
    for i, team in enumerate(teams_list):
        print(f"{i+1}. {team["title"]}")

    print("")
    home = int(input("Pick a home team(1-20): "))
    away = int(input("Pick an away team(1-20): "))

    return {"home": teams_list[home-1], "away": teams_list[away-1]}


def main():
    """main function"""
    teams_list = find_pl_teams()
    # match = display_teams(teams_list)
    # print(f"{match["home"]["title"]} vs. {match["away"]["title"]}")
    find_squad_list(teams_list[3])


if __name__ == "__main__":
    main()
