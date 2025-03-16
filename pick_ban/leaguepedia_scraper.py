import requests
from bs4 import BeautifulSoup
import pandas as pd


# comp = "LCP 2025 Season Kickoff"
# url = "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LCP+2025+Season+Kickoff&PBH%5Bteam%5D=&PBH%5Btextonly%5D%5Bis_checkbox%5D=true&PBH%5Btextonly%5D%5Bvalue%5D=&_run=&pfRunQueryFormName=PickBanHistory&wpRunQuery=&pf_free_text="
comp = "First_Stand_2025"
url = "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=First+Stand+2025&PBH%5Bteam%5D=&PBH%5Btextonly%5D%5Bis_checkbox%5D=true&PBH%5Btextonly%5D%5Bvalue%5D=&_run=&pfRunQueryFormName=PickBanHistory&wpRunQuery=&pf_free_text="

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find_all("table", class_="wikitable")


df = pd.read_html(str(table))[0]
df.columns = [col[1] for col in df.columns] 
print(df.head())


df.to_csv(f"picks_and_bans_{comp}.csv", index=False)
