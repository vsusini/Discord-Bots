import os
import discord
import requests
from datetime import datetime

from dotenv import load_dotenv

from discord.ext import commands
from discord import app_commands
import asyncio
import json
from enum import Enum

from collections import deque

load_dotenv()

headersToDeploy = {
  "Accept": "application/json,application/xml",
  "Content-Type": "application/json",
}

headers = {'User-Agent': 'Mozilla/5.0'}

class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def on_ready(self):
    print(f"Logged in as {self.user}")
    await self.updateGame("Payout per SFB")
    while True:
      await self.change_bot_nickname()
      await asyncio.sleep(60*10) #Timer in seconds on how often to update dashboard. 

  async def updateGame(self, string):
    print(string)
    await self.change_presence(status=discord.Status.online,
                              activity=discord.Activity(
                                  type=discord.ActivityType.watching,
                                  name=str(string)))
    
  async def change_bot_nickname(self):
        # Change the bot's nickname in the current server
        try:
            solPayout = getData()
            formatted_solPayout = f'{solPayout:,}'
            formatted_string = formatted_solPayout+" Sol"
            for guild in self.guilds:
                await guild.me.edit(nick=formatted_string)
                print(f"Changed bot nickname in {guild.name} to {formatted_string}")
        except discord.errors.Forbidden:
            print("I don't have permission to change my nickname in some server.")
        except discord.errors.HTTPException:
            print(f"Failed to change my nickname in {guild.name} server.")
        except Exception:
            await guild.me.edit(nick="🔴 Error")

client = MyClient(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

def getData():
    key = "https://sfb-backend-service-mainnet.up.railway.app/api/plinko/stats/weekly-fees"

    LAMPORTS_PER_SOL = 1000000000
    
    try:
        # requesting data from URL
        data = requests.get(key)  
        data = data.json()
        solPayout = round((float(data[0]['total_fees']) / LAMPORTS_PER_SOL * 0.35 / 100), 3)
        return solPayout
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "🔴 Error"

      
client.run(os.environ['DISCORD-TOKEN'])
