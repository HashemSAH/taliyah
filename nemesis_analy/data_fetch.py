import requests
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

API_KEY = 'RGAPI-bb3f400a-1d2b-402d-a892-00382a74bf3b'
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
    'start': 45, 
    'count': 45,  # Fetch the last x matches 
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
    
    opp_team_id = info_participants[opp_p_num]['teamId']

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


    # GET TIMELINE INFO
    timeline_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[idx]}/timeline'
    response = requests.get(timeline_url, headers={"X-Riot-Token": API_KEY})
    timeline_data = response.json()

    # Get participant ID from index (1-based)
    my_pid = info_participants[p_num]['participantId']
    opp_pid = info_participants[opp_p_num]['participantId']

    me_gold_over_time = [frame['participantFrames'][str(my_pid)]['totalGold']
    for frame in timeline_data['info']['frames']]
    opp_gold_over_time = [frame['participantFrames'][str(opp_pid)]['totalGold']
    for frame in timeline_data['info']['frames']]
    
    me_xp_over_time = [frame['participantFrames'][str(my_pid)]['xp']
    for frame in timeline_data['info']['frames']]
    opp_xp_over_time = [frame['participantFrames'][str(opp_pid)]['xp']
    for frame in timeline_data['info']['frames']]

    events = []
    for frame in timeline_data['info']['frames']:
        events.extend(frame['events'])
    elite_kills = [e for e in events if e['type'] == 'ELITE_MONSTER_KILL']


    objectives_by_team = defaultdict(list)
    objectives_count_by_team = defaultdict(lambda: defaultdict(int))
    first_grub_team = None
    first_dragon_team = None

    for event in elite_kills:
        monster = event['monsterType']
        team_id = event['killerTeamId']
        time = round(event['timestamp'] / 60000, 2)
        sub_type = event.get('monsterSubType', '')

        # Log kill
        objectives_by_team[team_id].append({
            'type': monster,
            'sub_type': sub_type,
            'time': time
        })

        # Count objectives
        objectives_count_by_team[team_id][monster] += 1

    def to_dict(obj):
        if isinstance(obj, defaultdict):
            return {k: to_dict(v) for k, v in obj.items()}
        return obj


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
        'gold_me': [me_gold_over_time],
        'xp_me': [me_xp_over_time],
        'gold_opp': [opp_gold_over_time],
        'xp_opp': [opp_xp_over_time],
        'objs_me': [to_dict(objectives_count_by_team[my_team_id])],
        'objs_opp': [to_dict(objectives_count_by_team[opp_team_id])],
        'my_team_id': [my_team_id],
        'obj_timeline': [to_dict(objectives_by_team)]
    }

    df = pd.concat([df, pd.DataFrame(row)], ignore_index=True)




df.to_csv('neme_data2_1.csv', index=False)  # Set index=False to avoid writing row indices


