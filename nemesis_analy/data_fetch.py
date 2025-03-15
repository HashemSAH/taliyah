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

match_ids = response.json()


df = pd.DataFrame(columns=[
    'Champ', 'Damage_done', 'Damage_taken', 'Gold_earned', 
    'Match_length', 'Minions_slain', 'Monsters_killed', 
    'Deaths', 'Win', 'Lane'
])


for idx in tqdm(range(len(match_ids))):
    # GET MATCH INFO
    match_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[idx]}'
    response = requests.get(match_url, headers={"X-Riot-Token": API_KEY})
    match_data = response.json()

    metadata_participants = match_data['metadata']['participants']
    info_participants = match_data['info']['participants']

    # Get your participant index
    for j, pid in enumerate(metadata_participants):
        if pid == puuid:
            p_num = j
            break

    my_info = info_participants[p_num]
    my_team_id = my_info['teamId']
    my_lane = my_info['teamPosition']

    # Get opponent in same lane but opposite team
    opp_p_num = None
    for k, p in enumerate(info_participants):
        if p['teamPosition'] == my_lane and p['teamId'] != my_team_id:
            opp_p_num = k
            break

    # Total team damage
    dmg_tot = sum(p['totalDamageDealtToChampions'] for p in info_participants if p['teamId'] == my_team_id)

    champ = my_info['championName']
    dmg = my_info['totalDamageDealtToChampions']
    dmg_share = dmg / dmg_tot if dmg_tot > 0 else 0
    taken = my_info['totalDamageTaken']
    gold = my_info['goldEarned']
    match_time = match_data['info']['gameDuration'] / 60
    mion = my_info['totalMinionsKilled']
    winner = my_info['win']
    death = my_info['deaths']
    monsters = my_info['neutralMinionsKilled']
    pos = my_info['teamPosition']
    opp_champ = info_participants[opp_p_num]['championName']
    # first_drag = 
    # Num_drags = 
    # void = 


    # GET TIMELINE INFO
    timeline_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[idx]}/timeline'
    response = requests.get(timeline_url, headers={"X-Riot-Token": API_KEY})
    timeline_data = response.json()

    # Get participant ID from index (1-based)
    my_pid = info_participants[p_num]['participantId']
    opp_pid = info_participants[opp_p_num]['participantId']

    try:
        gold7me = timeline_data['info']['frames'][7]['participantFrames'][str(my_pid)]['totalGold']
        gold7opp = timeline_data['info']['frames'][7]['participantFrames'][str(opp_pid)]['totalGold']
        gold15me = timeline_data['info']['frames'][15]['participantFrames'][str(my_pid)]['totalGold']
        gold15opp = timeline_data['info']['frames'][15]['participantFrames'][str(opp_pid)]['totalGold']
        xp7me = timeline_data['info']['frames'][7]['participantFrames'][str(my_pid)]['xp']
        xp7opp = timeline_data['info']['frames'][7]['participantFrames'][str(opp_pid)]['xp']
        xp15me = timeline_data['info']['frames'][15]['participantFrames'][str(my_pid)]['xp']
        xp15opp = timeline_data['info']['frames'][15]['participantFrames'][str(opp_pid)]['xp']
    except KeyError:
        continue  # skip match if frame 7 or 15 doesn't exist

    row = {
        'Champ': [champ],
        'Opp_champ': [opp_champ],
        'Damage_done': [dmg],
        'Damage share': [dmg_share],
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

    df = pd.concat([df, pd.DataFrame(row)], ignore_index=True)




df.to_csv('neme_data.csv', index=False)  # Set index=False to avoid writing row indices


