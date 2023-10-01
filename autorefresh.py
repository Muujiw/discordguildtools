from sched import scheduler
import time
from datetime import datetime, timedelta
import db_connection as sql
import requests

# This script is to keep the access tokens of the users in the database up to date.

def run_script():
 
 try:
            query = f"SELECT * FROM discords"
            sql.query_database(query)
            clientId = '' # Your client ID here
            clientSecret = '' # Your client secret here
            redirectUri = '' # Your redirect URI here
            
            for row in sql.query_database(query):
                
             
             userId = row['discord_id']
             refreshToken = row['refresh_token']
             payload = {
                'refresh_token': refreshToken,
                'client_id': clientId,
                'client_secret': clientSecret,
                'grant_type': 'refresh_token',
                'redirect_uri': redirectUri,
                'scope': 'identify guilds.join',
            }
             endpoint = f"https://discordapp.com/api/v9/oauth2/token"
             headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                
            }
             response = requests.post(endpoint, data=payload, headers=headers)
             print(response.json())
             print(response.status_code)
             if response.status_code == 400:
                 query = f"DELETE FROM discords WHERE discord_id = {userId}"
                 sql.execute_query(query)
                 print('Deleted user ' + str(userId) + ' from the database.')
                 continue
             accessToken = response.json()['access_token']
             refreshToken = response.json()['refresh_token']
             
             
             
                
             query = f"UPDATE discords SET access_token = '{accessToken}', refresh_token = '{refreshToken}' WHERE discord_id = {userId}"
             sql.execute_query(query)
             print
 except Exception as e:
           
            print('Erreur:', e)
        
run_script()

while True:
    time.sleep( 48 * 60 * 60 )
    run_script()