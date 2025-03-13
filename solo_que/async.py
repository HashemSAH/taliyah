import requests
import pandas as pd
from tqdm.asyncio import tqdm
import aiohttp
import asyncio


API_KEY = 'RGAPI-40dc697c-fb62-4e32-b1bb-957dfeb4dd0c'
REGION = 'asia'

summoner_name = 'hashsmashpotato'
tag_line = 'JEBNG'

account_url = f'https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}'
response = requests.get(account_url, headers={"X-Riot-Token": API_KEY})
data = response.json()
def check_puiid(data):
    if "puiid" not in data:
        print("Alert: 'puiid' key is missing!")
puuid = data['puuid']
region2 = 'sea'
matches_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
params = {
    'queue': 420,
    'count': 36,# Fetch the last x matches
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


async def fetch_match(session, match_id):
    """Fetch match data asynchronously."""
    match_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_id}'
    async with session.get(match_url, headers={"X-Riot-Token": API_KEY}) as response:
        if response.status == 429:  # Rate limit exceeded
            print(f"🚨 Rate limit hit! Stopping all requests.")
            return "RATE_LIMIT_EXCEEDED"  # Signal to stop execution
        else: 
            return await response.json()

async def process_match(session, match_id):
    """Fetch and process match data."""
    match_data = await fetch_match(session, match_id)
    lis_p = match_data['metadata']['participants']
    p_num = next((i for i, p in enumerate(lis_p) if p == puuid), None)

    if p_num is None:
        return None  # Skip if PUUID not found

    participant = match_data['info']['participants'][p_num]
    return {
        'Champ': participant['championName'],
        'Damage_done': participant['totalDamageDealtToChampions'],
        'Damage_taken': participant['totalDamageTaken'],
        'Gold_earned': participant['goldEarned'],
        'Match_length': match_data['info']['gameDuration'] / 60,
        'Minions_slain': participant['totalMinionsKilled'],
        'Monsters_killed': participant['neutralMinionsKilled'],
        'Deaths': participant['deaths'],
        'Win': participant['win'],
        'Lane': participant['teamPosition']
    }

async def main():
    global df
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        for i, match_id in enumerate(tqdm(match_ids)):
            tasks.append(process_match(session, match_id))

            # Respect API rate limit: pause after every 20 requests
            if (i + 1) % 15 == 0:
                await asyncio.sleep(3)

        results = await asyncio.gather(*tasks)

    df = pd.concat([df, pd.DataFrame(results)], ignore_index=True)

# Run the event loop
loop = asyncio.get_event_loop()

if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

loop.run_until_complete(main())

# Print final DataFrame
print(df)
    
df.to_csv('new.csv', index=False)  # Set index=False to avoid writing row indices

    	
    


    
