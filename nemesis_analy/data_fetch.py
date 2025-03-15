import requests
import pandas as pd
from tqdm import tqdm
import time

API_KEY = 'RGAPI-1fe2e5fe-e520-40f2-b323-b22e01c7a0f2'
REGION = 'europe'

# Step 1: Get the Summoner's PUUID
summoner_name = 'Dzukill'
tag_line = 'KISS'


account_url = f'https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}'
response = requests.get(account_url, headers={"X-Riot-Token": API_KEY})
data = response.json()

puuid = data['puuid']

region2 = 'europe'

matches_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'

params = {
    'queue': 420,
    'start': 0, 
    'count': 50,  # Fetch the last x matches 
    'api_key': API_KEY
}

response = requests.get(matches_url, params=params)

#response = requests.get(matches_url, headers={"X-Riot-Token": API_KEY})
match_ids = response.json()


df = pd.DataFrame(columns=[
    'Champ', 'Damage_done', 'Damage_taken', 'Gold_earned', 
    'Match_length', 'Minions_slain', 'Monsters_killed', 
    'Deaths', 'Win', 'Lane'
])


for i in tqdm(range(len(match_ids))):
    # if i % 15==0 and i != 0:
    #     time.sleep(20)

    match_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[i]}'
    response = requests.get(match_url, headers={"X-Riot-Token": API_KEY})
    match_data = response.json()

    lis_p = match_data['metadata']['participants']

    p_num = 0 

    for i in range(len(lis_p)):
        if lis_p[i] == puuid:
            break 
        p_num += 1
    
    opp_p_num = 0 
    for i in range(len(match_data['info']['participants'])):
        pos = (match_data['info']['participants'][i]['teamPosition'])
        if pos ==  match_data['info']['participants'][p_num]['teamPosition'] and i != p_num:
            opp_p_num = i


    champ = match_data['info']['participants'][p_num]['championName']
    dmg = match_data['info']['participants'][p_num]['totalDamageDealtToChampions']
    taken = match_data['info']['participants'][p_num]['totalDamageTaken']
    gold = match_data['info']['participants'][p_num]['goldEarned']
    match_time = match_data['info']['gameDuration']/60
    mion = match_data['info']['participants'][p_num]['totalMinionsKilled']
    winner = match_data['info']['participants'][p_num]['win']
    death = match_data['info']['participants'][p_num]['deaths']
    monsters = (match_data['info']['participants'][p_num]['neutralMinionsKilled'])
    pos = (match_data['info']['participants'][p_num]['teamPosition'])
    opp_champ = match_data['info']['participants'][opp_p_num]['championName']



    match_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[i]}/timeline'
    response = requests.get(match_url, headers={"X-Riot-Token": API_KEY})
    match_data = response.json()

    if opp_p_num == 0:    
        gold7me = match_data['info']["frames"][7]["participantFrames"][str(p_num)]["totalGold"] 
        gold7opp = '-'
        gold15me = match_data['info']["frames"][15]["participantFrames"][str(p_num)]["totalGold"] 
        gold15opp = '-'

        xp7me = match_data['info']["frames"][7]["participantFrames"][str(p_num)]["xp"] 
        xp7opp = '-'
        xp15me = match_data['info']["frames"][15]["participantFrames"][str(p_num)]["xp"]
        xp15opp = '-'

    else:
        gold7me = match_data['info']["frames"][7]["participantFrames"][str(p_num)]["totalGold"] 
        gold7opp = match_data['info']["frames"][7]["participantFrames"][str(opp_p_num)]["totalGold"]
        gold15me = match_data['info']["frames"][15]["participantFrames"][str(p_num)]["totalGold"] 
        gold15opp = match_data['info']["frames"][15]["participantFrames"][str(opp_p_num)]["totalGold"]

        xp7me = match_data['info']["frames"][7]["participantFrames"][str(p_num)]["xp"] 
        xp7opp = match_data['info']["frames"][7]["participantFrames"][str(opp_p_num)]["xp"] 
        xp15me = match_data['info']["frames"][15]["participantFrames"][str(p_num)]["xp"]
        xp15opp = match_data['info']["frames"][15]["participantFrames"][str(opp_p_num)]["xp"]
    
    row = {
        'Champ': [champ],
        'Opp_champ': [opp_champ],
        'Damage_done': [dmg],
        'Damage_taken': [taken],
        'Gold_earned': [gold],
        'Match_length': [match_time],
        'Minions_slain': [mion],
        'Monsters_killed': [monsters],
        'Deaths': [death],
        'Win': [winner],
        'Lane': [pos],
        'gold7me': [gold7me],
        'gold15me': [gold15me],
        'xp7me': [xp7me],
        'xp15me': [xp15me],
        'gold7opp': [gold7opp],
        'gold15opp': [gold15opp],
        'xp7opp': [xp7opp],
        'xp15opp': [xp15opp]

    }
    new_row_df = pd.DataFrame(row)

    # Append the new row to the existing DataFrame
    df = pd.concat([df, new_row_df], ignore_index=True)



df.to_csv('neme_data.csv', index=False)  # Set index=False to avoid writing row indices


