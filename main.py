import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load .env file (if using)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Store your token securely!


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

EVENT_DATE = datetime(2025, 8, 15)
CHANNEL_ID = os.getenv("CHANNEL_ID")

@bot.event
async def on_ready():
    channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
    print(f"Logged in as {bot.user}")

    if channel:
        days_left = get_days_left()
        message_content = f"🎉 FALTAN **{days_left} DÍAS PARA ADO!** 🎉"
        await channel.send(message_content)  # Send first countdown immediately

    countdown_loop.start()  # Start daily countdown updates




def get_days_left():
    today = datetime.now().date()
    event_day = EVENT_DATE.date()
    days_left = (event_day - today).days
    return days_left if days_left > 0 else 0 

@tasks.loop(hours=24)
async def countdown_loop():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        days_left = get_days_left()
        message_content = f"🎉 FALTAN **{days_left} DIAS PARA ADO🎉 @here"

        async for message in channel.history(limit=10):
            if message.author == bot.user:
                await message.edit(content = message_content)
                return
            
        await channel.send(message_content)


@countdown_loop.before_loop
async def before_countdown_loop():
    now = datetime.now()
    next_run = datetime.combine(now.date() + timedelta(days = 1), datetime.min.time())
    await discord.utils.sleep_until(next_run)



@bot.command(name="pang")  
async def pang(ctx):
    await ctx.send("Ping! 🏓")

bot.run(TOKEN)

