import requests
import discord

#This script shows all the servers where the bot is and the number of members in each server.

bot_token = '' # Your bot token here

intents = discord.Intents.default()
intents.guilds = True  
intents.members = True  
intents.message_content = True 

# Create a new client object
client = discord.Client(intents=intents)

@client.event
async def on_ready():
 def get_guild():
  reboot = 0
  while reboot == 0:
   for guild in client.guilds:
       print(guild.name)
       print(guild.id)
   reboot = 1
   while reboot == 1:
        
         
           getlist = input('Enter the server ID to get the number of members: ')
         
           endpoint = 'https://discord.com/api/v10/guilds/' + getlist + '/members?limit=1000'
         
           headers = {
             'Authorization': 'Bot ' + bot_token
           }
         
           response = requests.get(endpoint, headers=headers)
           
           text_response = response.text
           
           memberscount = text_response.count('joined_at')
           
           if memberscount >= 1000:
            print('\nThere are more than 1000 members on this server.\n')
           
           print('\nMembers: ' + str(memberscount) + '\n')
           
           memberscount = 0
           
           
             
           get_guild()
 get_guild()
client.run(bot_token)