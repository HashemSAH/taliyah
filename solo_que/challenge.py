import requests
import pandas as pd
from tqdm.asyncio import tqdm
# Replace with your own API key


API_KEY = 'RGAPI-5cc3f41f-9f1e-4ddb-8944-00c0e4bb9691'
REGION = 'europe'

# Step 1: Get the Summoner's PUUID
summoner_name = 'G2 Caps'
tag_line = '1323'


account_url = f'https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}'
response = requests.get(account_url, headers={"X-Riot-Token": API_KEY})
data = response.json()

def check_puiid(data):
    if "puiid" not in data:
        print("Alert: 'puiid' key is missing!")



puuid = data['puuid']

region2 = 'europe'

matches_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'

params = {
    'count': 5,  # Fetch the last x matches
    'api_key': API_KEY
}

response = requests.get(matches_url, params=params)

#response = requests.get(matches_url, headers={"X-Riot-Token": API_KEY})
match_ids = response.json()




# Print match data for the first match
for i in tqdm(range(len(match_ids))):
    match_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[i]}'
    response = requests.get(match_url, headers={"X-Riot-Token": API_KEY})
    match_data = response.json()

    lis_p = match_data['metadata']['participants']

    p_num = 0 

    for i in range(len(lis_p)):
        if lis_p[i] == puuid:
            break 
        p_num += 1

    print(match_data['info']['participants'][p_num]['challenges']['laningPhaseGoldExpAdvantage'])


    	
    


    
