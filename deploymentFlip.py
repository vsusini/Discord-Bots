import os
import discord
import requests
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

token = os.environ['api-token']

from urllib.request import urlopen, Request

headersToDeploy = {
  "Accept": "application/json,application/xml",
  'Content-Type': "application/json",
  "Authorization": token
}

clanId = "10952"

membersToAvoid = ["95"]


class Player:

  def __init__(self, id, name, recentPlayTime):
    self.id = id
    self.name = name
    self.recentPlayTime = recentPlayTime

  def __repr__(self) -> str:
    from pprint import pformat
    return pformat(vars(self), indent=4, width=1)


# async def deploy20RecentPlayers():
#   url = 'https://ev.io/group/10952/members'
#   headers = {'User-Agent': 'Mozilla/5.0'}
#   req = Request(url, headers=headers)
#   res = urlopen(req)
#   data = res.read().decode('utf8')

#   print("Gather Members from Clan, page 1")

#   inte = 0
#   clanMemberList = []
#   while inte >= 0:
#     inte = data.find("datatype="
#                      "", inte + 40)
#     singlePlayer = data[inte:inte + 40]
#     try:
#       playerName = singlePlayer.split(">")[1].split("<")[0]
#       #Print Player name
#       print(playerName)

#       filterUrl = "https://ev.io/jsonapi/user/user?filter[name]=" + playerName
#       response = requests.request("GET", filterUrl, headers=headers)
#       resData = response.json()
#       #print(resData["data"][0]["attributes"]["drupal_internal__uid"])
#       player = Player(
#         str(resData["data"][0]["attributes"]["drupal_internal__uid"]),
#         resData["data"][0]["attributes"]["display_name"],
#         resData["data"][0]["attributes"]["changed"])
#       clanMemberList.append(player)
#     except Exception as e:
#       print(e)
#       print("Hit the end of the members, next process.")

#   url = 'https://ev.io/group/10952/members?page=1'
#   req = Request(url, headers=headers)
#   res = urlopen(req)
#   data = res.read().decode('utf8')

#   print("Gather Members from Clan, page 2")

#   inte = 0
#   while inte >= 0:
#     inte = data.find("datatype="
#                      "", inte + 40)
#     singlePlayer = data[inte:inte + 40]
#     try:
#       playerName = singlePlayer.split(">")[1].split("<")[0]
#       #Print Player name
#       print(playerName)

#       filterUrl = "https://ev.io/jsonapi/user/user?filter[name]=" + playerName
#       response = requests.request("GET", filterUrl, headers=headers)
#       resData = response.json()
#       #print(resData["data"][0]["attributes"]["drupal_internal__uid"])
#       player = Player(
#         str(resData["data"][0]["attributes"]["drupal_internal__uid"]),
#         resData["data"][0]["attributes"]["display_name"],
#         resData["data"][0]["attributes"]["changed"])
#       clanMemberList.append(player)
#     except:
#       print("Hit the end of the members, next process.")

#   members = [i for i in clanMemberList if i.id not in membersToAvoid]

#   #List of members considered for deployment
#   #print(members)

#   print("Total Members Count: ", members.__len__())

#   try:
#     print("Gather Member Information")
#     clanMemberList.sort(key=lambda x: x.recentPlayTime, reverse=True)
#     top20Set = []
#     top20SetNames = []
#     print(clanMemberList)
#     for playerName in range(0, 20):
#       print("deploying: " + clanMemberList[playerName].name)
#       top20Set.append({"target_id": int(clanMemberList[playerName].id)})
#       top20SetNames.append(clanMemberList[playerName].name)

#     print("Sorted based on most recently played.")
#     payload = '{"id":[{"value":' + clanId + '}],"type":[{"target_id":"clan","target_type":"group_type"}],"field_deployed":' + top20Set.__str__(
#     ) + '}'
#     payload = payload.replace("'", '"', 40)
#     # Payload sent as data for the clan deployment
#     # print(payload)
#     url = "https://ev.io/group/" + clanId + "?_format=json"
#     # Fire off deployment to ev.io
#     response = requests.patch(url, data=payload, headers=headersToDeploy)
#     # To see response
#     print(response.json)
#     print("Clan: " + response.json()["label"][0]["value"])
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     print("Deployed at: " + current_time)
#     print("End of Deployment Loop ---------------------------")
#     return top20SetNames
#   except Exception as e:
#     print(e)
#     print("Error Occurred, retry soon.")


async def deploy20RecentPlayers():
  url = 'https://ev.io/group/10952/members'
  headers = {'User-Agent': 'Mozilla/5.0'}
  req = Request(url, headers=headers)
  res = urlopen(req)
  data = res.read().decode('utf8')

  print("Gather Members from Clan, page 1")

  inte = 0
  clanMemberList = []
  while inte >= 0:
    inte = data.find("datatype="
                     "", inte + 40)
    singlePlayer = data[inte:inte + 40]
    try:
      playerName = singlePlayer.split(">")[1].split("<")[0]
      #Print Player name
      print(playerName)

      filterUrl = "https://ev.io/jsonapi/user/user?filter[name]=" + playerName
      response = requests.request("GET", filterUrl, headers=headers)
      resData = response.json()
      #print(resData["data"][0]["attributes"]["drupal_internal__uid"])
      clanMemberList.append(
        str(resData["data"][0]["attributes"]["drupal_internal__uid"]))
    except:
      print("Hit the end of the members, next process.")

  url = 'https://ev.io/group/10952/members?page=1'
  req = Request(url, headers=headers)
  res = urlopen(req)
  data = res.read().decode('utf8')

  print("Gather Members from Clan, page 2")

  inte = 0
  while inte >= 0:
    inte = data.find("datatype="
                     "", inte + 40)
    singlePlayer = data[inte:inte + 40]
    try:
      playerName = singlePlayer.split(">")[1].split("<")[0]
      #Print Player name
      print(playerName)

      filterUrl = "https://ev.io/jsonapi/user/user?filter[name]=" + playerName
      response = requests.request("GET", filterUrl, headers=headers)
      resData = response.json()
      #print(resData["data"][0]["attributes"]["drupal_internal__uid"])
      clanMemberList.append(
        str(resData["data"][0]["attributes"]["drupal_internal__uid"]))
    except:
      print("Hit the end of the members, next process.")

  members = [i for i in clanMemberList if i not in membersToAvoid]

  #List of members considered for deployment
  print(members)

  print("Total Members Count: ", members.__len__())

  try:
    playerMap = []
    print("Gather Member Information")
    for playerName in members:
      playerUrl = "https://ev.io/user/" + playerName + "?_format=json"
      response = requests.request("GET", playerUrl, headers=headersToDeploy)
      data = response.json()
      player = Player(playerName, data["name"][0]["value"],
                      data["changed"][0]["value"])
      playerMap.append(player)

    playerMap.sort(key=lambda x: x.recentPlayTime, reverse=True)
    # print(playerMap)
    top20Set = []
    top20SetNames = []
    for playerName in range(0, 20):
      print("deploying: " + playerMap[playerName].name)
      top20Set.append({"target_id": int(playerMap[playerName].id)})
      top20SetNames.append(playerMap[playerName].name)

    print("Sorted based on most recently played.")
    payload = '{"id":[{"value":' + clanId + '}],"type":[{"target_id":"clan","target_type":"group_type"}],"field_deployed":' + top20Set.__str__(
    ) + '}'
    payload = payload.replace("'", '"', 40)
    # Payload sent as data for the clan deployment
    # print(payload)
    url = "https://ev.io/group/" + clanId + "?_format=json"
    # Fire off deployment to ev.io
    response = requests.patch(url, data=payload, headers=headersToDeploy)
    # To see response
    print(response.json)
    print("Clan: " + response.json()["label"][0]["value"])
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Deployed at: " + current_time)
    print("End of Deployment Loop ---------------------------")
    return top20SetNames
  except Exception as e:
    print(e)
    print("Error Occurred, retry soon.")


import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f"Logged in as {client.user}")
  #random message id
  message_id = 1087063164346171443
  while True:
    await updateGame("🟡Deploying")
    result = await deploy20RecentPlayers()
    message_id = await update_message(createDeploymentText(result), message_id)
    await updateGame("🟢Standby")
    await asyncio.sleep(180)


@client.event
async def on_message(message):
  # Ignore messages sent by the bot itself
  if message.author == client.user:
    return

  if message.content == 'ping':
    await message.channel.send('pong')


async def updateGame(string):
  print(string)
  await client.change_presence(status=discord.Status.online,
                               activity=discord.Activity(
                                 type=discord.ActivityType.watching,
                                 name=str(string)))


async def update_message(content, message_id):
  channel = client.get_channel(1087093790390636605)
  try:
    print("Trying to edit message.")
    message = await channel.fetch_message(message_id)
    await message.edit(embed=content)
  except:
    print("No Message Found, Creating Message")
    await channel.purge(limit=None)
    message = await channel.send(embed=content)
  return message.id


def createDeploymentText(list):
  print(list)
  url = "https://ev.io/group/" + clanId + "?_format=json"
  response = requests.request("GET", url, headers=headersToDeploy)
  data = response.json()
  one_word_per_line = '\n'.join(list)
  embed = discord.Embed(title="XBorg Deployment List",
                        url="https://ev.io/group/10952",
                        description="",
                        color=discord.Color.blue())
  # embed.set_author(name="XBorg Deployment List")
  embed.set_thumbnail(url=data["field_insignia"][0]["url"])
  embed.add_field(name="Deployed:",
                  value="\n>>> {}".format(one_word_per_line),
                  inline=False)
  embed.add_field(name="", value="Deployed <t:" + str(round(datetime.now().timestamp())) +
                   ":R>", inline=False)
  # embed.set_footer(text="Deployed at <t:" + str(round(datetime.now().timestamp())) +
  #                  ":R>")
  return embed


client.run(os.environ['TOKEN'])
