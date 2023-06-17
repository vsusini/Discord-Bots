import os
from zoneinfo import ZoneInfo
import discord
import requests
import json
from datetime import datetime

from dotenv import load_dotenv

from discord.ext import commands
from discord import app_commands
import asyncio

load_dotenv()

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json",
}

headers = {'User-Agent': 'Mozilla/5.0'}

guildId = 952044361334550548

from enum import Enum


class GameType(Enum):
    MLB = "MLB"
    NFL = "NFL"
    NHL = "NHL"
    NBA = "NBA"


class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def on_ready(self):
    print(f"Logged in as {self.user}")
    await self.updateGame("🟢Live")
    channel = self.get_channel(1099818961182412860)
    await tree.sync(guild= discord.Object(id=guildId))


  async def updateGame(self, string):
    print(string)
    await self.change_presence(status=discord.Status.online,
                              activity=discord.Activity(
                                  type=discord.ActivityType.watching,
                                  name=str(string)))

async def send_message(this,channel, content):
  await channel.send(content=content)

async def update_message(this, channel, content, message):
  if message == None:
    message = await channel.send(embed=content)
  else:
    print("Trying to edit message.")
    try:
      await message.edit(embed=content)
    except: 
      print("Message may be getting limited.")
      await asyncio.sleep(30)
      await message.edit(embed=content)
  return message

client = MyClient(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

#Lending
@tree.command(name = "test", description = "Rent a skin from the collection.", guild=discord.Object(id=guildId))
async def rent(interaction, type: GameType):
  #Check if the player exists.

  if (type == GameType.MLB):
    await createMLBText(interaction)

    
  
async def createMLBText(interaction):
  current_date = datetime.now(tz=ZoneInfo("America/New_York"))
  year = current_date.strftime("%Y")
  formatted_date = current_date.strftime("%Y-%m-%d")
    
  print(formatted_date)

  url = "https://v1.baseball.api-sports.io/games/?season="+year+"&league=1&date="+formatted_date+"&timezone=America/New_York"
  
  payload='{"league":'+"1"+'"}'
  payload = payload.replace("'", '"', 40)
  headers = {
    'x-rapidapi-key': os.environ['SPORT-TOKEN'],
    'x-rapidapi-host': 'v1.baseball.api-sports.io'
  }
  
  response = requests.request("GET", url, headers=headers)
  
  data = response.json()
  response = data['response']
  print(data)

  embed = discord.Embed(
        title="Live MLB Game Information",
        description="MLB Live Results for "+formatted_date,
        color=discord.Color.blue()
    )
  embed.set_thumbnail(url=response[0]["league"]["logo"])
  for game in response:
    embed.add_field(
    name=game["teams"]["home"]["name"] + " vs. " + game["teams"]["away"]["name"],
    value="\n>>> " +
          "Status: " + game["status"]["long"] +
          "\nScore: " + str(game["scores"]["home"]["total"]) + " - " + str(game["scores"]["away"]["total"]),
    inline=False
  )
  embed.set_footer(text="Games are updated every 15 seconds.")
  await interaction.response.send_message(embed=embed)
      
client.run(os.environ['DISCORD-TOKEN'])
