from bs4 import BeautifulSoup as bs
import requests as req
from pandas import DataFrame


def find_pl_teams() -> DataFrame:
    """
    find premier league teams from Transfermarkt
    along with their href which includes their unique ID
    """

    url = "https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1"
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


def display_teams(teams_list):
    for i, team in enumerate(teams_list):
        print(f"{i+1}. {team["title"]}")

    print("")
    home = int(input("Pick a home team(1-20): "))
    away = int(input("Pick an away team(1-20): "))

    return {"home": teams_list[home-1], "away": teams_list[away-1]}


def main():
    """main function"""
    teams_list = find_pl_teams()
    match = display_teams(teams_list)
    print(f"{match["home"]["title"]} vs. {match["away"]["title"]}")


if __name__ == "__main__":
    main()
