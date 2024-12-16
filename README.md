# Spotify Data Retrieval Project

## Overview
This Python script allows users to retrieve their Spotify library data, including saved albums, liked songs, and playlists using the Spotify Web API.

## Features
- Retrieve saved albums
- Fetch liked songs
- List user playlists
- OAuth 2.0 authentication with Spotify

## Prerequisites
- Python 3.7+
- `requests` library
- Spotify Developer Account
- Registered Spotify Application

## Setup and Installation

### 1. Dependencies
Install the required Python library:
```bash
pip install requests
```

### 2. Spotify Developer Credentials
1. Create a new application at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Obtain your:
   - Client ID
   - Client Secret
   - Redirect URI

### 3. Authentication Flow
This script follows the Spotify Authorization Code Flow:
- Generate an authorization URL
- User logs in and grants permissions
- Receive authorization code
- Exchange code for access token
- Make API requests with the token

## Usage

### Configuration
Replace the following variables in the script:
- `CLIENT_ID`: Your Spotify application's client ID
- `CLIENT_SECRET`: Your Spotify application's client secret
- `REDIRECT_URI`: Your registered redirect URI

### Running the Script
1. Authorize the application by opening the generated authorization URL
2. Copy the authorization code from the redirected URL
3. Replace `auth_code` with your received code
4. Run the script

## Security Notes
- Never commit sensitive information like client secrets to version control
- Use environment variables or a configuration file to store credentials
- Rotate your Spotify application credentials periodically

## Scopes Used
- `user-library-read`: Access user's saved albums and liked songs
- `playlist-read-private`: Read user's private playlists
- `user-read-private`: Access user's private profile information
- `user-read-email`: Read user's email address

## Error Handling
- Ensure valid credentials and active internet connection
- Check Spotify API response status for potential errors

## Limitations
- Access token expires after a short period
- Requires manual token refresh

## Contributing
Contributions, issues, and feature requests are welcome!

## License
This project is licensed under the MIT License. See the LICENSE file for details.
