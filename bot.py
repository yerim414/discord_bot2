import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from riot_api import RiotAPI

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"전적 봇 실행 : {bot.user}")


@bot.command(name="소환사")
async def summoner(ctx, *, summoner_name):
    await ctx.send(f"소환사 `{summoner_name}` 정보를 조회 중")
    riot = RiotAPI()
    puuid = riot.get_summoner_puuid(summoner_name)

    if puuid is None:
        await ctx.send("❌ 해당 소환사를 찾을 수 없습니다.")
        return

    info = riot.get_summoner_info_puuid(puuid)
    rank = riot.get_summoner_rank_puuid(puuid)

bot.run(DISCORD_TOKEN)