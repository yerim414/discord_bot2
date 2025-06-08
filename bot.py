import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from riot_api import get_summoner_info

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
    result = get_summoner_info(summoner_name) 

bot.run(DISCORD_TOKEN)