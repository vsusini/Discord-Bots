import os
import discord
import requests
from datetime import datetime

from dotenv import load_dotenv

from discord.ext import commands
from discord import app_commands
import asyncio

load_dotenv()

headersToDeploy = {
  "Accept": "application/json,application/xml",
  "Content-Type": "application/json",
}

headers = {'User-Agent': 'Mozilla/5.0'}

from enum import Enum

class RentType(Enum):
    Char = "Char"
    Sword = "Sword"
    AR = "AR"
    BR = "BR"
    LR = "LR"
    HC = "HC"


def determineTypeOfSkin(name: str):
  if "SW" in name:
    return SWSkins
  elif "AR" in name:
    return ARSkins
  elif "LR" in name:
    return LRSkins
  elif "BR" in name:
    return BRSkins
  elif "HC" in name:
    return HCSkins
  else:
    return charSkins

def determineTypeOfSkinWithSkinName(name: str):
  if "SW" in name:
    return RentType.Sword
  elif "AR" in name:
    return RentType.AR
  elif "LR" in name:
    return RentType.LR
  elif "BR" in name:
    return RentType.BR
  elif "HC" in name:
    return RentType.HC
  else:
    return RentType.Char

def determineTypeOfSkinByEnum(name: RentType):
  if name == RentType.Sword:
    return SWSkins
  elif name == RentType.AR:
    return ARSkins
  elif name == RentType.LR:
    return LRSkins
  elif name == RentType.BR:
    return BRSkins
  elif name == RentType.HC:
    return HCSkins
  else:
    return charSkins

def determineTypeOfSkinByEnumForActive(name: RentType):
  if name == RentType.Sword:
    return activeSWSkins
  elif name == RentType.AR:
    return activeARSkins
  elif name == RentType.LR:
    return activeLRSkins
  elif name == RentType.BR:
    return activeBRSkins
  elif name == RentType.HC:
    return activeHCSkins
  else:
    return activecharSkins

def ifSkinLent(name):
  if name == '':
    return False
  return True;

def search_array(array, attribute, value):
    for obj in array:
        if getattr(obj, attribute) == value:
            return obj
    return None

def findSkinToLend(array):
    for obj in array:
        if getattr(obj, "scholar") == "" and getattr(obj, "earnedToday") < SKIN_CAP:
            return obj
    return None

class Lender:

  def __init__(self, id, ownerID):
    self.id = id
    self.ownerID = ownerID

  def __repr__(self) -> str:
    from pprint import pformat
    return pformat(vars(self), indent=4, width=1)

class Skin:

  def __init__(self, id, name, address, scholar, owner, ownerID, earnedToday, tier):
    self.id = id
    self.name = name
    self.address = address
    self.scholar = scholar
    self.owner = owner
    self.ownerID = ownerID
    self.earnedToday = earnedToday
    self.tier = tier
    self.lent = ifSkinLent(scholar)

  def __repr__(self) -> str:
    from pprint import pformat
    return pformat(vars(self), indent=4, width=1)

SKIN_CAP = 2450
clanId = "10952"
guildId = 1060597181624627284

# Lenders=[Lender(328369, os.environ['FLIP-LENDER-KEY']), Lender(744782, os.environ['RAF-LENDER-KEY'])]
# Lenders=[Lender(744782, os.environ['RAF-LENDER-KEY']), Lender(613812, os.environ['LENDER-FLIP-LENDER-KEY'])]
Lenders=[Lender(744782, os.environ['RAF-LENDER-KEY'])]
skins = []
charSkins = []
ARSkins = []
LRSkins = []
BRSkins = []
SWSkins = []
HCSkins = []

from collections import deque

activeARSkins = deque()
activeLRSkins = deque()
activeBRSkins = deque()
activeSWSkins = deque()
activeHCSkins = deque()
activecharSkins = deque()

message_char = None
message_sword = None
message_HC = None
message_AR = None
message_LR = None
message_BR = None

class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def on_ready(self):
    print(f"Logged in as {self.user}")
    message_char = None
    message_sword = None
    message_HC = None
    message_AR = None
    message_LR = None
    message_BR = None
    await self.updateGame("🟢Live")
    channel = self.get_channel(1099818961182412860)
    await channel.purge(limit=None)
    await tree.sync(guild= discord.Object(id=guildId))
    while True:
      await self.updateGame("🟡Updating Dashboard")
      gatherSkins()
      message_char = await update_message(self, channel, createDisplayTextForArr(charSkins, "Character"), message_char)
      message_sword = await update_message(self, channel, createDisplayTextForArr(SWSkins, "Sword"),  message_sword)
      message_HC = await update_message(self, channel, createDisplayTextForArr(HCSkins, "HC"),  message_HC)
      message_AR = await update_message(self, channel, createDisplayTextForArr(ARSkins, "AR"), message_AR)
      message_LR = await update_message(self, channel, createDisplayTextForArr(LRSkins, "LR"), message_LR)
      message_BR = await update_message(self, channel, createDisplayTextForArr(BRSkins, "BR"), message_BR)
      await self.updateGame("🟢Live")
      await asyncio.sleep(600) #Timer in seconds on how often to update dashboard. 

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

def displayForRented(skin: Skin):
  if skin.earnedToday > SKIN_CAP:
    return "🟡"
  if skin.scholar == "":
    return "🟢"
  else:
    return "🔴"

def createDisplayTextForArr(arr, title):
  list = []
  sorted_skin_array = sorted(arr, key=lambda skin: skin.name)
  for skin in sorted_skin_array:
    list.append(displayForRented(skin)+ "  "+skin.name+" ("+skin.tier+")")
  url = "https://ev.io/group/" + clanId + "?_format=json"
  response = requests.request("GET", url, headers=headersToDeploy)
  data = response.json()
  if len(list) == 0:
    stringResult = "No Skins"
  else:
    one_word_per_line = '\n'.join(list)
    stringResult = "\n>>> {}".format(one_word_per_line)
  embed = discord.Embed(title="XBorg Skin List",
                        url="https://ev.io/group/10952",
                        description="",
                        color=discord.Color.blue())
  # embed.set_author(name="XBorg Deployment List")
  embed.set_thumbnail(url=data["field_insignia"][0]["url"])
  embed.add_field(name=title+" Skins:",
                  value=stringResult,
                  inline=False)
  embed.add_field(name="", value="Updated <t:" + str(round(datetime.now().timestamp())) +
                   ":R>", inline=False)
  # embed.set_footer(text="Deployed at <t:" + str(round(datetime.now().timestamp())) +
  #                  ":R>")
  return embed

client = MyClient(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

lendURL = 'https://web3.ev.io:2096/lend'
stopLendURL = 'https://web3.ev.io:2096/lend-stop'

#Lending
@tree.command(name = "rent", description = "Rent a skin from the collection.", guild=discord.Object(id=guildId))
async def rent(interaction, skin: RentType, name: str):
  #Check if the player exists.
  filterUrl = "https://ev.io/jsonapi/user/user?filter[name]=" + name
  response = requests.request("GET", filterUrl, headers=headers)
  resultPlayerResponse = response.json()
  if resultPlayerResponse["data"] == []:
    await interaction.response.send_message(f'A player with the name {name} does not exist.')
    return
  
  # Check if already has a skin to their name
  skinArr = determineTypeOfSkinByEnum(skin)
  if len(skinArr) == 0:
    await interaction.response.send_message(f'Uh oh, no skins in the {skin.name} type available.')
    return
  activeSkinArr = determineTypeOfSkinByEnumForActive(skin)
  result = search_array(activeSkinArr, "scholar", name.lower())
  if result != None:
    await interaction.response.send_message(f'There is already a {result.name} rented to {name}. Please /unlend.')
    return
    
  #Check if a skin exists to give to them.
  skinResult = findSkinToLend(skinArr)
  if skinResult == None:
    print("Couldn't find an available skin. Taking from queue.")
    await interaction.response.send_message("Couldn't find an available skin. Taking from queue.")
    skinObj, oldScholar = await removeSkinAndLend(skin, name.lower(), str(resultPlayerResponse["data"][0]["attributes"]["drupal_internal__uid"]))
    string = 'A '+str(skinObj.name)+' was removed from '+str(oldScholar)+". \n" 
    string = string + 'A '+skinObj.name+' lent to '+name+'.'
    await send_message(client, interaction.channel, string)
  else:
    print(f"Attempting to lend  {skinResult.address} to {name}")
    await interaction.response.send_message(f'A {skinResult.name} has been rented to {name}')
    lend(skinResult, name, str(resultPlayerResponse["data"][0]["attributes"]["drupal_internal__uid"]), skin)
    # await interaction.response.send_message(f'A {skinResult.name} has been rented to {name}')

def lend(skin: Skin, name: str, uid: str, type: RentType):

  payload = '{"uid":'+uid+',"nftAddress":"'+skin.address+'","flagId":'+skin.id+', "percentage":"60","ownerID":"'+skin.ownerID+'"}'
  payload = payload.replace("'", '"', 40)
  # Payload sent as data for the clan deployment
  # Fire off deployment to ev.io
  response = requests.post(lendURL, data=payload, headers=headersToDeploy)
  # To see response
  skinArr = determineTypeOfSkinByEnum(type)
  resultSkin = search_array(skinArr, "id", skin.id)
  resultSkin.scholar = name
  skin.scholar = name
  activeArr = determineTypeOfSkinByEnumForActive(type)
  activeArr.append(skin)
  print(response.json)
  print(f'A {skin.name} has been rented to {name}.')

#Unlending
@tree.command(name = "unlend", description = "Remove the desired skin from your list.", guild=discord.Object(id=guildId))
async def unlendSkin(interaction, skin: RentType, name: str):
  skinArr = determineTypeOfSkinByEnumForActive(skin)
  result = search_array(skinArr, "scholar", name.lower())
  if result == None:
    await interaction.response.send_message(f'There is no {str(skin.name)} to unlend.')
  else:
    print(f"Attempting to unlend  {result.address} from {name}")
    unlend(result.id, result.address, result.ownerID)
    skinArr = determineTypeOfSkinByEnum(skin)
    resultSkin = search_array(skinArr, "id", result.id)
    if resultSkin == None:
      print("error occured.")
    else:
      resultSkin.scholar = ""
      result.scholar = ""
    name_to_remove = result.id
    activeArr = determineTypeOfSkinByEnumForActive(type)
    for i in range(len(activeArr)):
      if activeArr[i].id == name_to_remove:
        del activeArr[i]
        break
    await interaction.response.send_message('The '+result.name+' has been removed from '+name)


def unlend(flagId: int, nftAddress: str, ownerID: str):
  payload = '{"flagId":'+str(flagId)+',"nftAddress":'+'"'+nftAddress+'"'+',"ownerID":'+'"'+ownerID+'"'+'}'
  response = requests.post(stopLendURL, data=payload, headers=headersToDeploy)
  print(response.json)

#Deals with the situation of all skins taken. 
async def removeSkinAndLend(skin: RentType, name: str, uid: int):
  activeSkinsArr = determineTypeOfSkinByEnumForActive(determineTypeOfSkinWithSkinName(skin.name))
  result = activeSkinsArr.popleft()
  oldScholar = result.scholar
  print(f'A {skin.name} has be removed from {result.scholar}.')
  unlend(result.id, result.address, result.ownerID)
  result.scholar = ""
  skinArr = determineTypeOfSkinByEnum(type)
  resultSkin = search_array(skinArr, "id", result.id)
  if resultSkin == None:
    print("error occured in getting the resultSkin")
  else:
    resultSkin.scholar = name
  lend(result, name, uid, skin)
  return result, oldScholar

import json

#Collects all the skins in the system. 
def gatherSkins():
    charSkins.clear()
    ARSkins.clear()
    LRSkins.clear()
    BRSkins.clear()
    SWSkins.clear()
    HCSkins.clear()

    activeARSkins.clear()
    activeLRSkins.clear()
    activeBRSkins.clear()
    activeSWSkins.clear()
    activeHCSkins.clear()
    activecharSkins.clear()
    for obj in Lenders:
      filterUrl = "https://ev.io/flags/" + str(obj.id)
      response = requests.request("GET", filterUrl, headers=headers)
      resData = response.json()
      for item in resData:
        # Checks if NFT and if earn is 1 
        if (item["field_meta"] != [] and not json.loads(item["field_meta"][0])["value"]["attributes"][4]["value"] == 1):
          meta_data = json.loads(item["field_meta"][0])
          skinsArr = determineTypeOfSkin(item["field_skin"])
          activeSkinsArr = determineTypeOfSkinByEnumForActive(determineTypeOfSkinWithSkinName(item["field_skin"]))
          if item["field_earned_today"] == "":
            earnedToday = 0
          else:
            earnedToday = int(item["field_earned_today"])
          skinsArr.append(Skin(item["id"],item["field_skin"],item["field_flag_nft_address"],item["field_scholar"].lower(), obj.id, obj.ownerID, earnedToday, meta_data["value"]["attributes"][1]["value"])) 
          if item["field_scholar"] != "":          
            activeSkinsArr.append(Skin(item["id"],item["field_skin"],item["field_flag_nft_address"],item["field_scholar"].lower(), obj.id, obj.ownerID, earnedToday, meta_data["value"]["attributes"][1]["value"])) 
    #print views to see who has which skins
    #print(activeLRSkins)

      
client.run(os.environ['DISCORD-TOKEN'])
