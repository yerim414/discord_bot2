import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from riot_api import RiotAPI
from datetime import datetime

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

QUEUE_ID_MAP = {
    420: "솔로랭크",
    430: "일반",
    440: "자유랭크",
    450: "칼바람",
    900: "우르프",
    700: "격전",
    1020: "단일 챔피언 모드",
    # 필요에 따라 추가 가능
}

@bot.event
async def on_ready():
    print(f"전적 봇 실행 : {bot.user}")

# TODO : 소스 정리 필요
@bot.command(name="소환사")
async def summoner(ctx, *, summoner_name):
    await ctx.send(f"🔎 소환사 `{summoner_name}` 정보를 조회 중")
    riot = RiotAPI()
    puuid = riot.get_summoner_puuid(summoner_name)

    if puuid is None:
        await ctx.send("❌ 해당 소환사를 찾을 수 없습니다.")
        return
    
    info = riot.get_summoner_info_puuid(puuid)
    rank = riot.get_summoner_rank_puuid(puuid)
    matchIds = riot.get_recent_match_ids(puuid, count=3)

    if matchIds:
        game_summary = []
        for id in matchIds:
            matchData = riot.get_match_detail(id)
            if not matchData:
                continue
            infoData = matchData.get("info", {})
            participants = infoData.get("participants", [])
            queueId = infoData.get("queueId", 0)
            gameMode = QUEUE_ID_MAP.get(queueId, f"알 수 없음({queueId})")
            for p in participants:
                if p["puuid"] == puuid:
                    champ = p["championName"]
                    kda = f"{p['kills']}/{p['deaths']}/{p['assists']}"
                    win = "승" if p["win"] else "패"
                    gameDuration = int(infoData["gameDuration"] / 60)
                    summary = f"{gameMode} | {champ} | {kda} | {gameDuration}분 | {win}"
                    game_summary.append(summary)
                    break

    soloRank = next((e for e in rank if e["queueType"] == "RANKED_SOLO_5x5"), None)
    dt = datetime.fromtimestamp(info.get("revisionDate") / 1000)

    # embed mapping
    embed = discord.Embed(
        title=f"{summoner_name} 님",
        description=f"> 갱신일 *{dt.strftime('%Y-%m-%d %H:%M:%S')}*",
        color=discord.Color.blue(),
        timestamp=datetime.now()
        )

    embed.set_author(
        name=f"{summoner_name} 님의 정보",
        icon_url=riot.get_Icon(info.get("profileIconId", 0))
    )

    embed.add_field(name="레벨", value=info.get("summonerLevel", "N/A"), inline=True)

    if soloRank:
        wins, losses = soloRank["wins"], soloRank["losses"]
        winRate = round((wins/(wins+losses))*100, 2)
        tierInfo = f"{soloRank['tier']} {soloRank['rank']} ({soloRank['leaguePoints']} LP)"
        embed.add_field(name="티어", value=tierInfo, inline=True)
        embed.add_field(name="전적", value=f"{wins}승 {losses}패 (승률 {winRate}%)")
    else:
        embed.add_field(name="랭크", value="Unranked", inline=True)

    if game_summary:
        recent_text = "\n".join([f"`{i+1} : {line}`" for i, line in enumerate(game_summary)])
        embed.add_field(name="⚔️ 최근 3게임 요약", value=recent_text, inline=False)

    embed.set_footer(text="롤 전적 검색", icon_url="https://slate.dan.onl/slate.png")
    await ctx.send(embed=embed)
    
bot.run(DISCORD_TOKEN)