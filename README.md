# Discord Guild API Tools

A collection of seven scripts to aid in Discord API interactions, necessitating a solid understanding of databases (SQL), Python, and APIs at large. These scripts encompass examples and utilities for database interactions, managing Discord guilds, and handling Discord OAuth2 authentication. Through these scripts, you can automate various tasks like refreshing OAuth tokens, managing member data, sending Direct Messages (DMs), and more, leveraging the power of Discord's robust API alongside a structured database setup.

## Table of Contents

1. [InsertDataExample.php](#insertdataexamplephp)
2. [Main.py](#mainpy)
3. [Db_connection.py](#db_connectionpy)
4. [dms.py](#dmspy)
5. [getguilds.py](#getguildspy)
6. [autorefresh.py](#autorefreshpy)
7. [SQLDatabaseCreationExample.txt](#sqldatabasecreationexampletxt)

### InsertDataExample.php

`InsertDataExample.php` is a PHP script showcasing how to handle Discord OAuth2 redirection to your webhook, and how to subsequently insert or update user data in your database.

#### Usage:

1. Include your database connection file at the beginning of the script:
    ```php
    include 'sql.php';  // Connection to your database
    ```

2. Specify your Discord application credentials and the redirect URI:
    ```php
    $clientId = ''; // Your client ID
    $clientSecret = ''; // Your client secret
    $redirectUri = ''; // Your redirect URI
    ```

3. The script checks if the authorization code is received from Discord:
    ```php
    if (isset($_GET['code'])) {
        $code = $_GET['code'];
        ...
    }
    ```

4. If the authorization code is present, the script will make a POST request to Discord API to obtain the access token:
    ```php
    $postData = array(
        'client_id' => $clientId,
        'client_secret' => $clientSecret,
        ...
    );
    ...
    $response = curl_exec($curl);
    ...
    ```

5. Upon receiving the access token, it will make a GET request to fetch the user information:
    ```php
    $curl = curl_init('https://discord.com/api/users/@me');
    ...
    $response = curl_exec($curl);
    ...
    ```

6. The script then checks if the user is already present in the database, if yes it updates the tokens, if not it inserts the new user data into the database:
    ```php
    $checkifuserifalreadyindatabase = $conn->prepare("SELECT * FROM discords WHERE discord_id = ?");
    ...
    if ($checkifuserifalreadyindatabase->num_rows > 0) {
        ...
    } else {
        ...
    }
    ```

The snippets above are simplified and demonstrate the core logic flow within `InsertDataExample.php`. Of course, this is just an example to explain how we get authorizations from the discord users.

---

## Main.py

### Requirements

Before running the scripts, ensure you have the following Python libraries installed:

1. **Discord.py**:
    ```bash
    pip install discord.py
    ```
2. **Requests**:
    ```bash
    pip install requests
    ```

Additionally, ensure you have a file named `db_connection.py` with the necessary functions for interacting with your database.

### Installing Dependencies:

You can install the required libraries using pip:

```bash
python3 -m pip install -U py-cord
pip install requests
# If you use MySQL
pip install mysql-connector-python
```

`Main.py` is a Python script that interacts with your database and facilitates various operations within a specific Discord server, such as adding members to the server, checking the number of members waiting to be added, and more.

#### Usage:

1. Import the necessary libraries and modules at the beginning of your script:
    ```python
    import discord
    import datetime
    import requests
    import db_connection as sql
    from discord.ext import commands
    ```

2. Define your server ID, bot token, and Discord application credentials:
    ```python
    serverId = ''  # ID of your server
    bot_token = ''  # Token of your bot
    clientId = ''  # Client ID of your application
    clientSecret = ''  # Client secret of your application
    redirectUri = ''  # Redirect URI of your application
    ```

3. Create a bot object with the necessary intents:
    ```python
    intents = discord.Intents.default()
    intents.guilds = True  
    intents.members = True  
    intents.message_content = True 
    bot = commands.Bot(intents=intents)
    ```

4. Define a function to check for administrator permissions:
    ```python
    def has_admin_permissions(user):
        if isinstance(user, discord.Member):
            return user.guild_permissions.administrator
        return False
    ```

5. Create event handlers for various bot events such as `on_ready`, `on_member_remove`, and define slash commands like `/lancer`, `/check`, `/forcejoin`, and `/all` to interact with the database and manage server members:
    ```python
    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')
    ...
    @bot.slash_command(name="lancer", guild_ids=[serverId], description="...")
    async def commandname(message):
        ...
    ```

    For instance, the `/lancer` command adds members who authorized the bot to the server if they waited 3 days:
    ```python
    @bot.slash_command(name = "lancer", guild_ids = [serverId], description = "...")
    async def commandname(message):
        ...
        query = f"SELECT * FROM discords WHERE joined = 0 AND date < '{date_str}'"
        results = sql.query_database(query)
        ...
    ```

6. Finally, run the bot using the `bot.run()` method:
    ```python
    bot.run(bot_token)
    ```

The snippets above outline the key aspects of `Main.py`. The script makes extensive use of the Discord.py library and interacts with the database to manage user data and server membership.

---

Continue with the next script [Db_connection.py](#db_connectionpy) as per the order in the Table of Contents.

## Db_connection.py

`Db_connection.py` is a script that facilitates the connection between the other scripts and a MySQL database. This script contains functions to establish a connection, execute queries, and close the connection. While this example utilizes MySQL, you can modify the script to work with other types of databases.

#### Usage:

1. **Creating a Database Connection**:
    ```python
    def create_connection():
        ...
        connection = mysql.connector.connect(
            host='',  # Your host here if you are not using localhost
            user='',  # Your user here
            password='',  # Your password here
            database=''  # Your database here
        )
        ...
    ```

    - Replace the placeholder values with your actual database credentials.
    - This function attempts to establish a connection to the MySQL database and returns the connection object if successful.

2. **Executing Queries that Return Data**:
    ```python
    def query_database(query):
        ...
        cursor.execute(query)
        results = cursor.fetchall()
        ...
    ```

    - Use this function to execute SQL queries that return data, such as SELECT queries.
    - It returns the query results as a list of dictionaries, where each dictionary corresponds to a row in the result set.

3. **Executing Queries that Do Not Return Data**:
    ```python
    def execute_query(query):
        ...
        cursor.execute(query)
        connection.commit()  # Commit the changes to the database
        ...
    ```

    - Use this function to execute SQL queries that do not return data, such as INSERT, UPDATE, or DELETE queries.
    - It commits the changes to the database.

**Note**:
If you are using a different type of database, you will need to adjust the connection parameters and potentially the query execution functions to match the syntax and functionality of your chosen database system.

---

Continue with the next script [dms.py](#dmspy) as per the order in the Table of Contents.

## dms.py

`dms.py` is a script designed to direct message (DM) all members of a specified Discord server. It requires your bot token and the server ID where you want to send the messages.

#### Usage:

1. **Setting Up Credentials**:
    ```python
    serverId = ''  # The server ID where you want to DM all members
    bot_token = ''  # Your bot token here
    ```

2. **Configuring Client Intents**:
    ```python
    intents = discord.Intents.default()
    intents.guilds = True  # To receive server-related events
    intents.members = True  # To receive member-related events
    intents.message_content = True  # To receive message-related events
    client = discord.Client(intents=intents)
    ```

3. **Executing on Ready Event**:
    ```python
    @client.event
    async def on_ready():
        ...
        send_dms(args.last_member_id)
    ```

    - Once the bot is ready, it triggers the `send_dms` function which will handle sending DMs to all server members.

4. **Sending DMs**:
    ```python
    def send_dms(last_member_id):
        ...
        for id in user_ids:
            ...
            payload = {
                'embed': {
                    "title": "Congratulations !",
                    ...
                    "description": "...",
                    ...
                }
            }
            ...
            response = requests.post(endpoint, headers=headers, json=payload)
            ...
    ```

    - The `send_dms` function is a recursive function that fetches member IDs from the server, creates a DM channel with each member, and sends an embedded message to each member.

5. **Rate Limiting**:
    ```python
    time.sleep(0.8)
    ```

    - A delay of 0.8 seconds is added between each DM to adhere to rate limits set by Discord's API.

6. **Running the Bot**:
    ```python
    client.run(bot_token)
    ```

    - This line starts the bot, allowing it to connect to Discord and begin sending DMs once ready.

**Note**:
The script makes use of the `requests` library to send HTTP requests to Discord's API. Ensure you have this library installed before running the script.

---

Continue with the next script [getguilds.py](#getguildspy) as per the order in the Table of Contents.

## getguilds.py

`getguilds.py` is a script that retrieves all the servers (guilds) your bot is a part of. Additionally, it provides an option to enter a specific server ID to fetch and display the number of members in that server.

#### Usage:

1. **Setting Up Bot Token**:
    ```python
    bot_token = ''  # Your bot token here
    ```

2. **Configuring Client Intents**:
    ```python
    intents = discord.Intents.default()
    intents.guilds = True  
    intents.members = True  
    intents.message_content = True 
    client = discord.Client(intents=intents)
    ```

3. **Defining on_ready Event**:
    ```python
    @client.event
    async def on_ready():
        def get_guild():
            ...
        get_guild()
    ```

    - Once the bot is ready, it calls the `get_guild` function which handles the main functionality of the script.

4. **Listing All Guilds**:
    ```python
    for guild in client.guilds:
        print(guild.name)
        print(guild.id)
    ```

    - This part of the `get_guild` function lists all the guilds along with their IDs where your bot is a member of.

5. **Fetching Member Count of a Specific Guild**:
    ```python
    getlist = input('Enter the server ID to get the number of members: ')
    endpoint = 'https://discord.com/api/v10/guilds/' + getlist + '/members?limit=1000'
    ...
    memberscount = text_response.count('joined_at')
    print('\nMembers: ' + str(memberscount) + '\n')
    ```

    - Prompt the user to enter a server ID, then send a request to Discord's API to get member data, and count the occurrences of 'joined_at' to estimate the number of members. Note that this method provides an estimate and is not accurate for guilds with more than 1000 members.

6. **Running the Bot**:
    ```python
    client.run(bot_token)
    ```

    - This line starts the bot, allowing it to connect to Discord and begin listing guilds once ready.

**Note**:
The script utilizes a while-loop to repeatedly prompt the user for a server ID and fetch the member count. It's important to handle inputs and exceptions carefully to avoid infinite loops or crashes.

---

Continue with the next script [autorefresh.py](#autorefreshpy) as per the order in the Table of Contents.

## autorefresh.py

`autorefresh.py` is a script aimed at keeping the access tokens of users in the database up-to-date by refreshing them periodically. This is crucial to ensure continuous interaction with the Discord API using the stored tokens.

#### Usage:

1. **Setting Up Credentials**:
    ```python
    clientId = '' # Your client ID here
    clientSecret = '' # Your client secret here
    redirectUri = '' # Your redirect URI here
    ```

2. **Defining the Main Function**:
    ```python
    def run_script():
        ...
        for row in sql.query_database(query):
            ...
            payload = {
                'refresh_token': refreshToken,
                ...
            }
            ...
            response = requests.post(endpoint, data=payload, headers=headers)
            ...
    ```

    - The `run_script` function iterates through all the records in the `discords` table, and attempts to refresh the access token for each user using the refresh token stored in the database.

3. **Handling Token Refresh**:
    ```python
    accessToken = response.json()['access_token']
    refreshToken = response.json()['refresh_token']
    query = f"UPDATE discords SET access_token = '{accessToken}', refresh_token = '{refreshToken}' WHERE discord_id = {userId}"
    sql.execute_query(query)
    ```

    - If the token refresh is successful, the new access and refresh tokens are updated in the database.

4. **Handling Failed Refreshes**:
    ```python
    if response.status_code == 400:
        query = f"DELETE FROM discords WHERE discord_id = {userId}"
        sql.execute_query(query)
        print('Deleted user ' + str(userId) + ' from the database.')
    ```

    - If the token refresh fails (e.g., because the refresh token is no longer valid), the corresponding user record is deleted from the database.

5. **Periodic Execution**:
    ```python
    while True:
        time.sleep( 48 * 60 * 60 )
        run_script()
    ```

    - The script enters an infinite loop where the `run_script` function is called every 48 hours to refresh the tokens.

**Note**:
This script makes HTTP requests to Discord's OAuth2 token endpoint to refresh tokens, and interacts with the database to update the token records. Ensure that your database connection script (`db_connection.py`) is properly set up, and the necessary libraries (`requests`) are installed.

---

Proceed to the next script [SQLDatabaseCreationExample.txt](#sqldatabasecreationexampletxt) as per the order in the Table of Contents.

## SQLDatabaseCreationExample.txt

`SQLDatabaseCreationExample.txt` is a text file containing SQL commands to create a database and a table required for the project. These scripts provide a structured way to store and manage data about Discord users and their tokens.

### Database and Table Creation:

1. **Creating Database**:
    ```sql
    CREATE DATABASE 'discord';
    USE 'discord';
    ```

    - The above commands create a new database named `'discord'` and select it for use.

2. **Creating Table**:
    ```sql
    CREATE TABLE `discords` (
      `id` int(11) NOT NULL,
      `discord_id` bigint(20) DEFAULT NULL,
      `access_token` text NOT NULL,
      `date` timestamp NOT NULL DEFAULT current_timestamp(),
      `joined` tinyint(4) NOT NULL DEFAULT 0,
      `refresh_token` text DEFAULT NULL,
      `hak` text DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ```

    - A table named `discords` is created with various fields to store data like Discord user ID, access token, refresh token, and more.

3. **Setting Up Indexes and Primary Key**:
    ```sql
    ALTER TABLE `discords`
      ADD PRIMARY KEY (`id`);
    ```

    - A primary key is set on the `id` field to ensure unique identification of records.

4. **Setting Up Auto-Increment**:
    ```sql
    ALTER TABLE `discords`
      MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=301;
    COMMIT;
    ```

    - The `id` field is set to auto-increment, starting at 301, to automatically assign a unique identifier to new records.

5. **Character Set and Collation Configuration** (optional):
    ```sql
    /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
    /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
    /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
    ```

    - These commands restore previous character set and collation configurations. It's optional and not required for the creation of the database or table.

**Note**:
Make sure to replace `'discord'` with your desired database name, and adjust the field definitions in the `CREATE TABLE` statement as needed to match your project requirements.

---






