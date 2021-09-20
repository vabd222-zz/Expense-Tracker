import discord
import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

#MongoDB connnection
cluster = MongoClient("mongodb+srv://admin:BIbmQooEiBQOhyqC@expensetrackercluster.k3ir5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Expenses"]
users = db["Users"]
expenses = db["Expenses"]


#connecting to discord client
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

#listenting to events

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content=="pong":
        return

@client.event
async def on_member_join(member):
  for channel in member.guild.channels:
    if str(channel)=="general":
      await channel.send(f"""Welcome to the server {member.mention}""")
      query={"userId":str(member)}
      result = users.insert_one(query)

@client.event
async def on_member_remove(member):
  for channel in member.guild.channels:
    if str(channel)=="general":
      await channel.send(f"""{member.mention} Left the server""")
      query = {"userId":str(member)}
      result = users.delete_one(query)




#acessing discord bot token
client.run(os.getenv('BOT_TOKEN'))