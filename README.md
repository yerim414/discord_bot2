# Discord LoL Info Bot

Python 기반 디스코드 봇으로, Riot API를 사용해 리그 오브 레전드 유저 정보를 조회하고 디스코드 채팅으로 보여줍니다.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blue)

## 소개
이 봇은 Riot Games API를 통해 소환사 정보를 불러오고, 디스코드 채팅창에 출력합니다.  
소환사 랭크, 레벨, 최근 시즌 정보를 간단한 명령어로 확인할 수 있습니다.

## 설치 및 실행
```bash
# 저장소 클론
git clone https://github.com/yerim414/discord_bot2.git
cd discord_bot2

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일 생성)
echo "DISCORD_TOKEN=디스코드_봇_토큰" >> .env
echo "RIOT_API_KEY=라이엇_API_키" >> .env

# 봇 실행
python main.py