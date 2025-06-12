import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class RiotAPI():
    def __init__(self):
        try:
            self.api_key = os.getenv("RIOT_API_KEY")
            print(self.api_key)
            self.headers = {"X-Riot-Token": self.api_key}
            self.api_url = "https://kr.api.riotgames.com"
            self.asia_url = "https://asia.api.riotgames.com"
        except Exception as e:
            # TODO : 에러처리 필요
            print("필요한 정보가 누락 되었습니다.")
            return None

    def _get_request(self, url, param = None):
        response = requests.get(
            url = url,
            params = param,
            headers = self.headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            # TODO : 에러처리 필요
            print("에러처리 필요")
            return None

    def get_summoner_puuid(self, summoner_name: str, tag_line: str = "KR1"):
        # puuid 발급
        url = f"{self.asia_url}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
        result = self._get_request(url)
        return result.get("puuid", None)

    def get_summoner_info_puuid(self, puuid: str):
        # 소환사 정보
        url = f"{self.api_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        result = self._get_request(url)
        return result

    def get_summoner_rank_puuid(self, puuid: str):
        # 현재 시즌 티어 정보
        url = f"{self.api_url}/lol/league/v4/entries/by-puuid/{puuid}"
        result = self._get_request(url)
        return result
    
    def get_Icon(self, ID: int):
        return f"https://ddragon.leagueoflegends.com/cdn/14.11.1/img/profileicon/{ID}.png"
    
    def get_recent_match_ids(self, puuid, count=3):
        url = f"{self.asia_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {"count": count}
        return self._get_request(url, params)
    
    def get_match_detail(self, match_id):
        url = f"{self.asia_url}/lol/match/v5/matches/{match_id}"
        return self._get_request(url)