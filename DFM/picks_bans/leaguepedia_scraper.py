import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LCP+2025+Season+Kickoff%09&PBH%5Bteam%5D=DetonatioN+FocusMe&PBH%5Btextonly%5D%5Bis_checkbox%5D=true&PBH%5Btextonly%5D%5Bvalue%5D=&_run=&pfRunQueryFormName=PickBanHistory&wpRunQuery=&pf_free_text="


headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find_all("table", class_="wikitable")


df = pd.read_html(str(table))[0]
df.columns = [col[1] for col in df.columns] 
print(df.head())


df.to_csv(f"DFM_picks_and_bans_LCP2025_1.csv", index=False)
