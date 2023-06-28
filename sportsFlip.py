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

baseballMap = {'Arizona Diamondbacks': 2, 
          'Atlanta Braves': 3, 
          'Baltimore Orioles': 4,
          'Boston Red Sox': 5,
          'Chicago Cubs': 6,
          'Chicago White Sox': 7,
          'Cincinati Reds': 8,
          'Cleveland Indians': 9,
          'Colorado Rockies': 10,
          'Detriot Tigers': 12,
          'Houston Astros': 15,
          'Kansas City Royals': 16,
          'Los Angles Angels': 17,
          'Los Angles Dodgers': 18,
          'Miami Marlins': 19,
          'Milwaukee Brewers': 20,
          'Minnesota Twins': 22,
          'New York Mets': 24,
          'New York Yankees': 25,
          'Oakland Athletics': 26,
          'Philadelphia Phillies': 27,
          'Pittsburgh Pirates': 28,
          'San Diego Padres': 30,
          'San Francisco Giants': 31,
          'Seattle Mariners': 32,
          'St Louis Cardinals': 33,
          'Tampa Bay Rays': 34,
          'Texas Rangers': 35,
          'Toronto Blue Jays': 36,
          'Washington Nationals': 37}

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

@tree.command(name = "get-games", description = "Get live scores for todays event", guild=discord.Object(id=guildId))
async def rent(interaction, type: GameType):

  if currentTeams == []:
    await interaction.response.send_message("No on-going events to display data for")

  if (currentGameType == GameType.MLB):
    await createMLBText(interaction)
  if (currentGameType == GameType.NBA):
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")
  if (currentGameType == GameType.NHL):
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")
  if (currentGameType == GameType.NFL):
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")

@tree.command(name = "create-one-team-event", description = "Create an event with 1 game involved", guild=discord.Object(id=guildId))
async def help(interaction, type: GameType, team_in_game: str):
    if await checkIfValidUser(interaction):
      return
    
    gameTypeMap = await determineTypeMap(interaction, type)
    
    teamNames = []
    keys = []

    teamNames.append(team_in_game)

    for name in teamNames:
      lower_keys = [key.lower() for key in gameTypeMap.keys()]
      if name.lower() not in lower_keys:
          await interaction.response.send_message("Invalid option "+team_in_game+". Please select a valid option. Format Example: Toronto Blue Jays", ephemeral=True)
          return
        
      matched_key = list(gameTypeMap.keys())[lower_keys.index(team_in_game.lower())]
      keys.append(matched_key)

    global currentGameType 
    global currentTeams 
    currentGameType = type
    for key in keys:
      currentTeams.append(gameTypeMap[key])
    await interaction.response.send_message(f"Successfully storing games for sport: {currentGameType} and team: {currentTeams}", ephemeral=True)

@tree.command(name = "create-two-team-event", description = "Create an event with 1 game involved", guild=discord.Object(id=guildId))
async def help(interaction, type: GameType, team_in_game1: str, team_in_game2: str):
    if await checkIfValidUser(interaction):
      return
    
    gameTypeMap = await determineTypeMap(interaction, type)
    
    teamNames = []
    keys = []

    teamNames.append(team_in_game1)
    teamNames.append(team_in_game2)

    for name in teamNames:
      lower_keys = [key.lower() for key in gameTypeMap.keys()]
      if name.lower() not in lower_keys:
          await interaction.response.send_message("Invalid option "+name+". Please select a valid option. Format Example: Toronto Blue Jays", ephemeral=True)
          return
        
      matched_key = list(gameTypeMap.keys())[lower_keys.index(name.lower())]
      keys.append(matched_key)

    global currentGameType 
    global currentTeams 
    currentGameType = type
    for key in keys:
      currentTeams.append(gameTypeMap[key])
    await interaction.response.send_message(f"Successfully storing games for sport: {currentGameType} and team: {currentTeams}", ephemeral=True)

@tree.command(name = "create-three-team-event", description = "Create an event with 1 game involved", guild=discord.Object(id=guildId))
async def help(interaction, type: GameType, team_in_game1: str, team_in_game2: str, team_in_game3: str):
    if await checkIfValidUser(interaction):
      return
    
    gameTypeMap = await determineTypeMap(interaction, type)
    
    teamNames = []
    keys = []

    teamNames.append(team_in_game1)
    teamNames.append(team_in_game2)
    teamNames.append(team_in_game3)

    for name in teamNames:
      lower_keys = [key.lower() for key in gameTypeMap.keys()]
      if name.lower() not in lower_keys:
          await interaction.response.send_message("Invalid option "+name+". Please select a valid option. Format Example: Toronto Blue Jays", ephemeral=True)
          return
        
      matched_key = list(gameTypeMap.keys())[lower_keys.index(name.lower())]
      keys.append(matched_key)

    global currentGameType 
    global currentTeams 
    currentGameType = type
    for key in keys:
      currentTeams.append(gameTypeMap[key])
    await interaction.response.send_message(f"Successfully storing games for sport: {currentGameType} and team: {currentTeams}", ephemeral=True)

async def determineTypeMap(interaction, type: GameType):
  if type == GameType.MLB:
    return baseballMap
  elif type == GameType.NBA:
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")
    return None
  elif type == GameType.NFL:
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")
    return None
  elif type == GameType.NHL:
    await interaction.response.send_message("Not available at the moment. Bug Flip :)")
    return None
  else:
    await interaction.response.send_message("Not sure how you got here.")
    return None

@tree.command(name = "get-flips-state", description = "Get the current state of the bot", guild=discord.Object(id=guildId))
async def help(interaction):
    if await checkIfValidUser(interaction):
      return
    await interaction.response.send_message(f"Storing games for sport: {currentGameType} and team: {currentTeams}", ephemeral=True)

@tree.command(name = "reset-state", description = "Reset back to no events state", guild=discord.Object(id=guildId))
async def reset(interaction):
    if await checkIfValidUser(interaction):
      return
    global currentGameType 
    currentGameType = None
    global currentTeams 
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
    if game["teams"]["home"]["id"] in currentTeams or game["teams"]["away"]["id"] in currentTeams:
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
