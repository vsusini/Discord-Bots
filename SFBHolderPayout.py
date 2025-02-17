import os
import re
import discord
import requests
from datetime import datetime
import subprocess

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
    self.channel_id = int(1250441182295756911) #SFB Channel ID

  async def on_ready(self):
    print(f"Logged in as {self.user}")
    await self.updateGame("Payout per SFB")
    while True:
      await self.change_bot_nickname()
      await asyncio.sleep(60*10) #Timer in seconds on how often to update dashboard. 

  async def updateGame(self, string):
    print("Updating presense...")
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
            formatted_string = formatted_solPayout+" SOL"
            for guild in self.guilds:
                await guild.me.edit(nick=formatted_string)
                print(f"Changed bot nickname in {guild.name} to {formatted_string}")
            await self.update_channel_name("Payout per SFB : "+formatted_string)
        except discord.errors.Forbidden:
            print("I don't have permission to change my nickname in some server.")
        except discord.errors.HTTPException:
            print(f"Failed to change my nickname in {guild.name} server.")
        except Exception:
            for guild in self.guilds:
                await guild.me.edit(nick="🔴 Error")
                print(f"🔴 Error")

  async def update_channel_name(self, new_name):
        # Update the channel name
        try:
            channel = self.get_channel(self.channel_id)
            if channel:
                await channel.edit(name=new_name)
                print(f"Updated channel name to {new_name}")
            else:
                print(f"Channel with ID {self.channel_id} not found")
        except discord.errors.Forbidden:
            print("I don't have permission to change the channel name.")
        except discord.errors.HTTPException as e:
            print(f"Failed to change the channel name: {e}")
        except Exception as e:
            print(f"An error occurred while updating the channel name: {str(e)}")

client = MyClient(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

def getData():
    
    try:
        # Getting values from solana cli
        plinkoTotal = subprocess.check_output(["solana", "balance", "8q3ymvGuCQ2fVjp22eCHDX1AvjwFVKU54eqS56VSbNV1", "-u", "mainnet-beta"], text=True)
        dashTotal = subprocess.check_output(["solana", "balance", "Dy9KfmcJzRjakx1AwRW29E2mwQrY1jy8zTJ3hZCzW7ea", "-u", "mainnet-beta"], text=True)
        # Remove SOL from output
        plinkoTotal = re.search(r"([\d.]+)", plinkoTotal)
        dashTotal = re.search(r"([\d.]+)", dashTotal)
         # Convert to floats and calculate payout.
        dashTotal = float(dashTotal.group(1))
        plinkoTotal = float(plinkoTotal.group(1))
        solPayout = round(((dashTotal+plinkoTotal) * 0.35 / 100), 3)
        return solPayout
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "🔴 Error"

      
client.run(os.environ['DISCORD-TOKEN'])
