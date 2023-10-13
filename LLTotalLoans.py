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
    await self.updateGame("LL Active Loans")
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
          loans = getData()
          formatted_loans = f'{loans:,.0f}'
          for guild in self.guilds:
              await guild.me.edit(nick=formatted_loans+" loans")
              print(f"Changed bot nickname in {guild.name} to {formatted_loans}")
        except discord.errors.Forbidden:
            print("I don't have permission to change my nickname in some server.")
        except discord.errors.HTTPException:
            print("Failed to change my nickname in some server.")

client = MyClient(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

def getData():
    key = "https://api.lenderlabs.xyz/api/get_ll_volume"
    
    try:
        # requesting data from URL
        data = requests.get(key)  
        data = data.json()
        loans = round(float(data['activeLoans']), 2)
        return loans
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "🔴 Error"

      
client.run(os.environ['DISCORD-TOKEN'])
