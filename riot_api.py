import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

HEADERS = {"X-Riot-Token": RIOT_API_KEY}
API_URL = f"https://asia.api.riotgames.com"

def get_summoner_info(summoner_name):
    tag_line = "KR1"
    url = f"{API_URL}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
    return requests.get(url, headers=HEADERS).json()