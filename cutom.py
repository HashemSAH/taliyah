
import requests


API_KEY = 'RGAPI-02249568-e7df-44ed-89c6-7c6dce7ccb78'



region2 = 'sea'
match_id = 'OC1_656847171'

match_url = f'https://{region2}.api.riotgames.com/lol/match/v5/matches/{match_id}'
response = requests.get(match_url, headers={"X-Riot-Token": API_KEY})
print(response.json())