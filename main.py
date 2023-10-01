import discord
import datetime
import requests
from datetime import datetime, timedelta
import db_connection as sql
from discord.ext import commands



serverId = '' # ID of your server
bot_token = '' # Token of your bot

now = datetime.now()

four_days_ago = now - timedelta(days=3)

date_str = four_days_ago.strftime('%Y-%m-%d %H:%M:%S')

# Set the intents to receive events from the server and the members
intents = discord.Intents.default()
intents.guilds = True  
intents.members = True  
intents.message_content = True 

# Create the bot object
bot = commands.Bot(intents=intents)


clientId = '' # Client ID of your application
clientSecret = '' # Client secret of your application
redirectUri = '' # Redirect URI of your application



def has_admin_permissions(user): # Check if the user has the administrator permission so the bot can spam the server without any problem
    if isinstance(user, discord.Member):
        return user.guild_permissions.administrator
    return False

# When the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    

    
@bot.event   
async def on_member_remove(member):
    # Get the user ID
    user_id = member.id
    print(user_id)
     
    query = f"UPDATE discords SET joined = 0 WHERE discord_id = {user_id}" # Set the joined value to 0 so the user will be added again when the command /lancer or /forcejoin is used
    
    sql.execute_query(query)

@bot.slash_command(name = "lancer", guild_ids = [serverId], description = "Adds members who authorized the bot to the server if they waited 3 days.") # /lancer command
# This is the stealth mode command, it will add members only if they authorized the bot more than 3 days ago
async def commandname(message):
    
    if has_admin_permissions(message.author):
        print('An admin used the /lancer command !')
        await message.respond('Starting the script !') # Send a message to the user who used the command
    
        now = datetime.now()
        four_days_ago = now - timedelta(days=3)
        date_str = four_days_ago.strftime('%Y-%m-%d %H:%M:%S')
        query = f"SELECT * FROM discords WHERE joined = 0 AND date < '{date_str}'"
        results = sql.query_database(query)
        if len(results) == 0:
           await message.send('There is no member to add !')
        for row in results:
            userId = row['discord_id']
            accessToken = row['access_token']
            payload = {
                'access_token': accessToken,
            }
            endpoint = f"https://discordapp.com/api/guilds/{serverId}/members/{userId}"
            headers = {
                'Authorization': f'Bot {bot_token}',
                'Content-Type': 'application/json',
            }
            response = requests.put(endpoint, json=payload, headers=headers)
            print(response.status_code)
            if response.status_code == 204 or response.status_code == 201:
                
                query = f"UPDATE discords SET joined = 1 WHERE discord_id = {userId}"
                sql.execute_query(query)                
            await message.channel.send(f'The member <@{userId}> has been added to the server.')
            
        
            
    
    else:
        await message.respond('You are not trusted enough to use this command !', ephemeral = True)
        
@bot.slash_command(name = "check", guild_ids = [serverId], description = "Check the number of members who are waiting to be added to the server.") # /check command
# This command will check the number of members who are waiting to be added to the server.
async def commandname(message):
  if has_admin_permissions(message.author):
    await message.respond('Here is the result !') # Send a message to the user who used the command
    print('An admin used the /check command !')
    try:
            now = datetime.now()

            four_days_ago = now - timedelta(days=3)

            date_str = four_days_ago.strftime('%Y-%m-%d %H:%M:%S')
            query = f"SELECT * FROM discords WHERE joined = 0 AND date < '{date_str}'"
            sql.query_database(query)
            usercount = len(sql.query_database(query))
            
            if usercount == 0 or usercount == 1:
                await message.channel.send(f'There is currently {usercount} member waiting to be added to the server.')
            else:
                
              await message.channel.send(f'There are currently {usercount} members waiting to be added to the server.')
            now = datetime.now()

            four_days_ago = now - timedelta(days=3)

            date_str = four_days_ago.strftime('%Y-%m-%d %H:%M:%S')
            query = f"SELECT * FROM discords WHERE joined = 0 AND date > '{date_str}'"
            sql.query_database(query)
            usercount = len(sql.query_database(query))
            
            if usercount == 0 or usercount == 1:
                await message.channel.send(f'There is currently {usercount} member waiting to be added to the server but who did not wait 3 days.')
            else:
                
                
                await message.channel.send(f'There are currently {usercount} members waiting to be added to the server but who did not wait 3 days.')
    except Exception as e:
            await message.channel.send('An error occurred while executing the script.')
            print('Erreur:', e)
  else:
        await message.respond('You are not trusted enough to use this command !', ephemeral = True)
            
@bot.slash_command(name = "forcejoin", guild_ids = [serverId], description = "Adds all members who authorized the bot to the server.") # /forcejoin command
# This command will add all the members who authorized the bot to the server
async def commandname(message):
    if has_admin_permissions(message.author):
        await message.respond('Let me think !') # Send a message to the user who used the command
        query = f"SELECT * FROM discords WHERE joined = 0"
        results = sql.query_database(query)
        if len(results) == 0:
           await message.channel.send('There is no member to add !')
        for row in results:
         try:
            userId = row['discord_id']
            accessToken = row['access_token']
            isJoined = row['joined']
            if isJoined == 0:
                payload = {
                'access_token': accessToken,
                }
                endpoint = f"https://discordapp.com/api/guilds/{serverId}/members/{userId}"
                headers = {
                'Authorization': f'Bot {bot_token}',
                'Content-Type': 'application/json',
                }
                response = requests.put(endpoint, json=payload, headers=headers)
                print(response.status_code)
                if response.status_code != 204 and response.status_code != 201:
                    await message.channel.send(f'An error occurred while adding the member <@{userId}> to the server.')
                    continue
                if response.status_code == 204 or response.status_code == 201:
                
                    query = f"UPDATE discords SET joined = 1 WHERE discord_id = {userId}"
                    sql.execute_query(query)
                    await message.channel.send(f'The member <@{userId}> has been added to the server.')
            else:
                    await message.channel.send(f'The member <@{userId}> has already been added to the server.')
                       
         except Exception as e:
            await message.channel.send('An error occurred while executing the script.')
            print('Erreur:', e)
         

            
 
    else:
        await message.respond('You are not trusted enough to use this command !', ephemeral = True)

@bot.slash_command(name = "all", guild_ids = [serverId], description = "Get the number of members who authorized the bot.") # /all command
# This command will give you the number of members who authorized the bot in the database
async def commandname(message):
    if has_admin_permissions(message.author):
        print('An admin used the /all command !')
        await message.respond('Here is the result !') # Send a message to the user who used the command
        query = f"SELECT * FROM discords"
        results = sql.query_database(query)
        await message.channel.send(f'There are currently {len(results)} members in the database.')
    
# Run the bot
bot.run(bot_token)




