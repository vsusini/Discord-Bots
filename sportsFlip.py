import os
from zoneinfo import ZoneInfo
import discord
import requests
import json
from datetime import datetime

from dotenv import load_dotenv

from discord.ext import commands
from discord import app_commands
from typing import List
import asyncio

load_dotenv()

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json",
}

headers = {'User-Agent': 'Mozilla/5.0'}

from enum import Enum

#Data

guildId = 952044361334550548


class GameType(Enum):
    MLB = "MLB"
    NFL = "NFL"
    NHL = "NHL"
    NBA = "NBA"

class Teams(Enum):
    Arizona_Diamondbacks = 2
    Atlanta_Braves = 3
    Baltimore_Orioles = 4
    Boston_Red_Sox = 5
    Chicago_Cubs = 6
    Chicago_White_Sox = 7
    Cincinati_Reds = 8
    Cleveland_Indians = 9
    Colorado_Rockies = 10
    Detriot_Tigers = 12
    Houston_Astros = 15
    Kansas_City_Royals = 16
    Los_Angles_Angels = 17
    Los_Angles_Dodgers = 18
    Miami_Marlins = 19
    Milwaukee_Brewers = 20
    Minnesota_Twins = 22
    New_York_Mets = 24
    New_York_Yankees = 25
    Oakland_Athletics = 26
    Philadelphia_Phillies = 27
    Pittsburgh_Pirates = 28
    San_Diego_Padres = 30
    San_Francisco_Giants = 31
    Seattle_Mariners = 32
    St_Louis_Cardinals = 33
    Tampa_Bay_Rays = 34
    Texas_Rangers = 35
    Toronto_Blue_Jays = 36
    Washington_Nationals = 37


currentGameType = None
currentTeams = []

# Code

class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def on_ready(self):
    print(f"Logged in as {self.user}")
    await self.updateGame("🟢Live")
    channel = self.get_channel(1099818961182412860)
    for guild in self.guilds:
      await tree.sync(guild= discord.Object(id=guild.id))


  async def updateGame(self, string):
    print(string)
    await self.change_presence(status=discord.Status.online,
                              activity=discord.Activity(
                                  type=discord.ActivityType.watching,
                                  name=str(string)))

client = MyClient(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@tree.command(name = "get_current_games", description = "Get today's scores for the specific sport", guild=discord.Object(id=guildId))
async def rent(interaction, type: GameType):

  if currentTeams == []:
    await interaction.response.send_message("No on-going games to display data for")

  if (currentGameType == GameType.MLB):
    await createMLBText(interaction)
  if (currentGameType == GameType.NBA):
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")
  if (currentGameType == GameType.NHL):
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")
  if (currentGameType == GameType.NFL):
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")

@tree.command(name = "create_game_one", description = "Get today's scores for the specific sport", guild=discord.Object(id=guildId))
async def help(interaction, type: GameType, team_in_game: Teams):
    if await checkIfValidUser(interaction):
      return
    currentGameType = type
    await interaction.response.send_message(f"Successfully storing games for sport: {currentGameType} and team: {currentTeams}", ephemeral=True)

@tree.command(name = "get_flips_state", description = "Get today's scores for the specific sport", guild=discord.Object(id=guildId))
async def help(interaction):
    if await checkIfValidUser(interaction):
      return
    await interaction.response.send_message(f"Storing games for sport: {currentGameType} and team: {currentTeams}", ephemeral=True)

@tree.command(name = "reset_state", description = "Get today's scores for the specific sport", guild=discord.Object(id=guildId))
async def reset(interaction):
    if await checkIfValidUser(interaction):
      return
    currentGameType = None
    currentTeams = []
    await interaction.response.send_message(f"I have been reset. Storing games for sport: {currentGameType} and teams: {currentTeams}", ephemeral=True)


async def checkIfValidUser(interaction):
  if "SF Master" not in [role.name for role in interaction.user.roles]:
      await interaction.response.send_message(f"Silly {interaction.user}, you don't have permissions to do this command!", ephemeral=True)
      return True
  return False
    
  
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
