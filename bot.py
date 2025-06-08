import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
# RIOT_TOKEN = os.getenv("RIOT_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"전적 봇 실행 : {bot.user}")


@bot.command(name="소환사")
async def summoner(ctx, *, summoner_name):
    print(summoner_name)
    await ctx.send(f"소환사 `{summoner_name}` 정보를 조회 중")

bot.run(DISCORD_TOKEN)