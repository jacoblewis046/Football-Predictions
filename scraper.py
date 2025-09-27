from bs4 import BeautifulSoup as bs
import requests as req
from pandas import DataFrame

URL = "https://www.scrapethissite.com/pages/forms/"

response = req.get(URL)

soup = bs(response.text, "html.parser")

table = soup.find("table", class_="table")

headers = [header.text.strip() for header in table.find_all("th")]

list_data = []

for row in table.find_all("tr", class_="team"):
    data = [data_col.text.strip() for data_col in row.find_all("td")]
    list_data.append(data)

# print(list_data)

df = DataFrame(data=list_data, columns=headers)
print(df)
