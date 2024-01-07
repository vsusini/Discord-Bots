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

guildId = 971056772104200322


class GameType(Enum):
    MLB = "MLB"
    NFL = "NFL"
    NHL = "NHL"
    NBA = "NBA"

hockeyMap = {
   'Anaheim Ducks': 670,
   'Arizona Coyotes': 671,
   'Boston Bruins': 673,
   'Buffalo Sabres': 674,
   'Calgary Flames': 675,
   'Carolina Hurricanes': 676,
   'Chicago Blackhawks': 678,
   'Colorado Avalanche': 679,
   'Columbus Blue Jackets': 680,
   'Dallas Stars': 681,
   'Detroit Red Wings': 682,
   'Edmonton Oilers': 683,
   'Florida Panthers': 684,
   'Los Angeles Kings': 685,
   'Minnesota Wild': 687,
   'Montreal Canadiens': 688,
   'Nashville Predators': 689,
   'New Jersey Devils': 690,
   'New York Islanders': 691,
   'New York Rangers': 692,
   'Ottawa Senators': 693,
   'Philadelphia Flyers': 695,
   'Pittsburgh Penguins': 696,
   'San Jose Sharks': 697,
   'St. Louis Blues': 698,
   'Tampa Bay Lightning': 699,
   'Toronto Maple Leafs': 700,
   'Vancouver Canucks': 701,
   'Vegas Golden Knights': 702,
   'Washington Capitals': 703,
   'Winnipeg Jets': 704,
   'Seattle Kraken': 1436
}

footballMap = {
  'Buffalo Bills': 20,
  'Miami Dolphins': 25,
  'New England Patriots': 3,
  'New York Jets': 13,
  'Cincinnati Bengals': 10,
  'Baltimore Ravens': 5,
  'Pittsburgh Steelers': 22,
  'Cleveland Browns': 9,
  'Jacksonville Jaguars': 2,
  'Tennessee Titans': 6,
  'Indianapolis Colts': 21,
  'Houston Texans': 26,
  'Kansas City Chiefs': 17,
  'Los Angeles Chargers': 30,
  'Las Vegas Raiders': 1,
  'Denver Broncos': 28,
  'Philadelphia Eagles': 12,
  'Dallas Cowboys': 29,
  'New York Giants': 4,
  'Washington Commanders': 18,
  'Minnesota Vikings': 32,
  'Detroit Lions': 7,
  'Green Bay Packers': 15,
  'Chicago Bears': 16,
  'Tampa Bay Buccaneers': 24,
  'Carolina Panthers': 19,
  'New Orleans Saints': 27,
  'Atlanta Falcons': 8,
  'San Francisco 49ers': 14,
  'Seattle Seahawks': 23,
  'Los Angeles Rams': 31,
  'Arizona Cardinals': 11,
}

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

basketBallMap = {'Atlanta Hawks': 132, 
          'Boston Celtics': 133, 
          'Brooklyn Nets': 134,
          'Charlotte Hornets': 135,
          'Chicago Bulls': 136,
          'Cleveland Cavaliers': 137,
          'Dallas Mavericks': 138,
          'Denver Nuggets': 139,
          'Detroit Pistons': 140,
          'Golden State Warriors': 141,
          'Houston Rockets': 142,
          'Indiana Pacers': 143,
          'Los Angeles Clippers': 144,
          'Los Angeles Lakers': 145,
          'Miami Heat': 147,
          'Milwaukee Bucks': 148,
          'Minnesota Timberwolves': 149,
          'New Orleans Pelicans': 150,
          'New York Knicks': 151,
          'Oklahoma City Thunder': 152,
          'Orlando Magic': 153,
          'Philadelphia 76ers': 154,
          'Phoenix Suns': 155,
          'Portland Trail Blazers': 156,
          'Sacramento Kings': 157,
          'San Antonio Spurs': 158,
          'Toronto Raptors': 159,
          'Utah Jazz': 160,
          'Washington Wizards': 161}


currentGameType = None
currentTeams = []
ADMIN_ROLE = "RF Master"

# Code

def get_team_names_from_ids(id_list, data_map):
    team_names = []

    for team_id in id_list:
        for name, team_id_in_map in data_map.items():
            if team_id == team_id_in_map:
                team_names.append(name)
                break
        else:
            team_names.append(None)  # Handle the case when ID is not found in the map

    return team_names

class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def on_ready(self):
    print(f"Logged in as {self.user}")
    await self.updateGame("🟢Live")
    channel = self.get_channel(1099818961182412860)
    for guild in self.guilds:
      await tree.sync(guild= discord.Object(id=guild.id))

  async def on_message(self, message):
    # don't respond to ourselves
    if message.author == self.user:
        return
    if 'soccer' in message.content.lower():
        await message.channel.send('football*')


  async def updateGame(self, string):
    print(string)
    await self.change_presence(status=discord.Status.online,
                              activity=discord.Activity(
                                  type=discord.ActivityType.watching,
                                  name=str(string)))
    
  async def on_guild_join(self, guild):
    # When the bot joins a new guild, create a new role
    role_name = ADMIN_ROLE
    permissions = discord.Permissions()  # You can customize the permissions here if needed
    new_role = await guild.create_role(name=role_name, permissions=permissions)
    # Optionally, you can customize the role color and other settings
    # new_role = await guild.create_role(name=role_name, permissions=permissions, colour=discord.Colour.orange(), hoist=True)
    print(f"Created a new role '{role_name}' in guild '{guild.name}'")
    for guild in self.guilds:
      await tree.sync(guild= discord.Object(id=guild.id))

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "get-games", description = "Get live scores for todays event", guild=discord.Object(id=guildId))
async def rent(interaction):

  if currentTeams == []:
    await interaction.response.send_message("No on-going events to display data for.")

  if (currentGameType == GameType.MLB):
    await createMLBText(interaction)
  if (currentGameType == GameType.NBA):
    await createNBAText(interaction)
  if (currentGameType == GameType.NHL):
    await createNHLText(interaction)
  if (currentGameType == GameType.NFL):
    await createNFLText(interaction)

@tree.command(name = "create-one-team-event", description = "Create an event with 1 team involved", guild=discord.Object(id=guildId))
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
    await interaction.response.send_message(f"Successfully storing games for sport: {currentGameType} and team: {get_team_names_from_ids(currentTeams, gameTypeMap)}", ephemeral=True)

@tree.command(name = "create-two-team-event", description = "Create an event with 2 teams involved", guild=discord.Object(id=guildId))
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
    await interaction.response.send_message(f"Successfully storing games for sport: {currentGameType} and team: {get_team_names_from_ids(currentTeams, gameTypeMap)}", ephemeral=True)

@tree.command(name = "create-three-team-event", description = "Create an event with 3 teams involved", guild=discord.Object(id=guildId))
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
    await interaction.response.send_message(f"Successfully storing games for sport: {currentGameType} and team: {get_team_names_from_ids(currentTeams, gameTypeMap)}", ephemeral=True)

async def determineTypeMap(interaction, type: GameType):
  if type == GameType.MLB:
    return baseballMap
  elif type == GameType.NBA:
    return basketBallMap
  elif type == GameType.NFL:
    return footballMap
  elif type == GameType.NHL:
    return hockeyMap
  else:
    await interaction.response.send_message("Not sure how you got here.")
    return None

@tree.command(name = "get-flips-state", description = "Get the current state of the bot", guild=discord.Object(id=guildId))
async def help(interaction):
    if await checkIfValidUser(interaction):
      return
    
    gameTypeMap = await determineTypeMap(interaction, currentGameType)

    await interaction.response.send_message(f"Storing games for sport: {currentGameType} and team: {get_team_names_from_ids(currentTeams, gameTypeMap)}", ephemeral=True)

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
  if ADMIN_ROLE not in [role.name for role in interaction.user.roles]:
      await interaction.response.send_message(f"Silly {interaction.user}, you don't have permissions to do this command!", ephemeral=True)
      return True
  return False
    
  
async def createMLBText(interaction):
  current_date = datetime.now(tz=ZoneInfo("HST"))
  year = current_date.strftime("%Y")
  formatted_date = current_date.strftime("%Y-%m-%d")

  url = "https://v1.baseball.api-sports.io/games/?season="+year+"&league=1&date="+formatted_date+"&timezone=HST"
  
  payload='{"league":'+"1"+'"}'
  payload = payload.replace("'", '"', 40)
  headers = {
    'x-rapidapi-key': os.environ['SPORT-TOKEN'],
    'x-rapidapi-host': 'v1.baseball.api-sports.io'
  }
  
  response = requests.request("GET", url, headers=headers)
  
  data = response.json()
  response = data['response']
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

async def createNBAText(interaction):
  current_date = datetime.now(tz=ZoneInfo("HST"))
  year = current_date.strftime("%Y")
  newYearRange = year + "-"+str(int(year)+1)
  formatted_date = current_date.strftime("%Y-%m-%d")

  url = "https://v1.basketball.api-sports.io/games/?season="+newYearRange+"&league=12&date="+formatted_date+"&timezone=HST"
  
  payload='{"league":'+"12"+'"}'
  payload = payload.replace("'", '"', 40)
  headers = {
    'x-rapidapi-key': os.environ['SPORT-TOKEN'],
    'x-rapidapi-host': 'v1.basketball.api-sports.io'
  }
  
  response = requests.request("GET", url, headers=headers)
  
  data = response.json()
  response = data['response']
  embed = discord.Embed(
        title="Live NBA Game Information",
        description="NBA Live Results for "+formatted_date,
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

async def createNFLText(interaction):
  current_date = datetime.now(tz=ZoneInfo("HST"))
  year = current_date.strftime("%Y")
  formatted_date = current_date.strftime("%Y-%m-%d")

  
  url = "https://v1.american-football.api-sports.io/games/?date="+formatted_date+"&timezone=HST"
  
  payload='{"league":'+"1"+'"}'
  payload = payload.replace("'", '"', 40)
  headers = {
    'x-rapidapi-key': os.environ['SPORT-TOKEN'],
    'x-rapidapi-host': 'v1.american-football.api-sports.io'
  }
  
  response = requests.request("GET", url, headers=headers)
  
  data = response.json()
  response = data['response']
  embed = discord.Embed(
        title="Live NFL Game Information",
        description="NFL Live Results for "+formatted_date,
        color=discord.Color.blue()
    )
  embed.set_thumbnail(url=response[0]["league"]["logo"])
  for game in response:
    if game["teams"]["home"]["id"] in currentTeams or game["teams"]["away"]["id"] in currentTeams:
      embed.add_field(
      name=game["teams"]["home"]["name"] + " vs. " + game["teams"]["away"]["name"],
      value="\n>>> " +
            "Status: " + game["game"]["status"]["long"] +
            "\nScore: " + str(game["scores"]["home"]["total"]) + " - " + str(game["scores"]["away"]["total"]),
      inline=False
  )
  embed.set_footer(text="Games are updated every 15 seconds.")
  await interaction.response.send_message(embed=embed)

async def createNHLText(interaction):
  current_date = datetime.now(tz=ZoneInfo("HST"))
  year = current_date.strftime("%Y")
  newYearRange = str(int(year)-1)
  formatted_date = current_date.strftime("%Y-%m-%d")

  url = "https://v1.hockey.api-sports.io/games/?season="+newYearRange+"&league=57&date="+formatted_date+"&timezone=HST"
  
  payload='{"league":'+"57"+'"}'
  payload = payload.replace("'", '"', 40)
  headers = {
    'x-rapidapi-key': os.environ['SPORT-TOKEN'],
    'x-rapidapi-host': 'v1.hockey.api-sports.io'
  }
  
  response = requests.request("GET", url, headers=headers)

  
  data = response.json()
  response = data['response']
  embed = discord.Embed(
        title="Live NHL Game Information",
        description="NHL Live Results for "+formatted_date,
        color=discord.Color.blue()
    )
  embed.set_thumbnail(url=response[0]["league"]["logo"])
  for game in response:
    if game["teams"]["home"]["id"] in currentTeams or game["teams"]["away"]["id"] in currentTeams:
      embed.add_field(
      name=game["teams"]["home"]["name"] + " vs. " + game["teams"]["away"]["name"],
      value="\n>>> " +
            "Status: " + game["status"]["long"] +
            "\nScore: " + str(game["scores"]["home"]) + " - " + str(game["scores"]["away"]),
      inline=False
  )
  embed.set_footer(text="Games are updated every 15 seconds.")
  await interaction.response.send_message(embed=embed)
      
client.run(os.environ['DISCORD-TOKEN'])
