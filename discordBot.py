import os
import discord
import requests


def getSolPrice():
  
    # defining key/request url
    key = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
  
    # requesting data from url
    data = requests.get(key)  
    data = data.json()
    solPrice = round(float(data['price']), 2)
    print(f"{data['symbol']} price is {solPrice}")
    return solPrice


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
        await self.updateGame(getSolPrice())


    async def on_message(self, message):
        await self.updateGame(getSolPrice())
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

    async def updateGame(self, price):
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="SOL Price: $"+str(price)))


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.environ['TOKEN'])
