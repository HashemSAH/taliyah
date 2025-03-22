import requests
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


    opp_p_num = None
    for k, p in enumerate(info_participants):
        if p['teamPosition'] == my_lane and p['teamId'] != my_team_id:
            opp_p_num = k
            break
    
    opp_team_id = info_participants[opp_p_num]['teamId']


    timeline_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_ids[i]}/timeline'
    response = requests.get(timeline_url, headers={"X-Riot-Token": API_KEY})
    timeline_data = response.json()
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
    
    print(to_dict(objectives_count_by_team))
    print(to_dict(objectives_by_team))


    
    # team_1_dragons = match_data['info']['teams'][0]['objectives']['dragon']['kills']
    # team_2_dragons = match_data['info']['teams'][1]['objectives']['dragon']['kills']

    # print(f"Team 1 Dragons: {team_1_dragons}")
    # print(f"Team 2 Dragons: {team_2_dragons}")

    # team_1_dragons = match_data['info']['teams'][0]['objectives']['dragon']['first']
    # team_2_dragons = match_data['info']['teams'][1]['objectives']['dragon']['first']

    # print(f"Team 1 Dragons: {team_1_dragons}")
    # print(f"Team 2 Dragons: {team_2_dragons}")

    

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
 
