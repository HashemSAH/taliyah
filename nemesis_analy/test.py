import requests


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
    'count': 30,  # Fetch the last x matches 
    'api_key': API_KEY
}

response = requests.get(matches_url, params=params)

match_ids = response.json()

for i in range(len(match_ids[:1])):
    match_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[i]}'
    response = requests.get(match_url, headers={"X-Riot-Token": API_KEY})
    match_data = response.json()
    team_1_dragons = match_data['info']['teams'][0]['objectives']['dragon']['kills']
    team_2_dragons = match_data['info']['teams'][1]['objectives']['dragon']['kills']

    print(f"Team 1 Dragons: {team_1_dragons}")
    print(f"Team 2 Dragons: {team_2_dragons}")

    team_1_dragons = match_data['info']['teams'][0]['objectives']['dragon']['first']
    team_2_dragons = match_data['info']['teams'][1]['objectives']['dragon']['first']

    print(f"Team 1 Dragons: {team_1_dragons}")
    print(f"Team 2 Dragons: {team_2_dragons}")

    

    # match_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[i]}/timeline'
    # response = requests.get(match_url, headers={"X-Riot-Token": API_KEY})
    # match_data = response.json()

    # lis_p = match_data['metadata']['participants']

    # p_num = 1 

    # for i in range(len(lis_p)):
    #     if lis_p[i] == puuid:
    #         break 
    #     p_num += 1


    # print(p_num, match_data['info']["frames"][7]["participantFrames"][str(p_num )])
    # if p_num > 5: 
    #     opp_p_num = p_num - 5
    # else: 
    #     opp_p_num = p_num + 5
    #print(opp_p_num, match_data['info']["frames"][7]["participantFrames"][str(opp_p_num)]['totalGold'])
 
