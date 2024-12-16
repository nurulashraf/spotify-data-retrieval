import requests
import base64

# Client ID and redirect URI - Replace with your Spotify Developer credentials
CLIENT_ID = ''  # Your Spotify Client ID
CLIENT_SECRET = ''  # Your Spotify Client Secret
REDIRECT_URI = ''  # Your Spotify Redirect URI

# Spotify Authorization URL
AUTH_URL = 'https://accounts.spotify.com/authorize'

# Authorization request parameters
params = {
    'client_id': CLIENT_ID,
    'response_type': 'code',
    'redirect_uri': REDIRECT_URI,
    'scope': 'user-library-read playlist-read-private user-read-private user-read-email'
}

# Generate the authorization URL
auth_request_url = f"{AUTH_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

# Prompt the user to visit the authorization URL
print("Please visit this URL and authorize the app:")
print(auth_request_url)

# Spotify API credentials and authorization code - Ensure `auth_code` is filled in after authorization
auth_code = ''  # Replace with the authorization code obtained after visiting the URL

# Encode the Client ID and Client Secret for token exchange
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
auth_bytes = auth_str.encode('utf-8')
auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

# Exchange the authorization code for an access token
auth_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': 'Basic ' + auth_base64,
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': REDIRECT_URI
}

# Make the request to Spotify for the access token
response = requests.post(auth_url, headers=headers, data=data)

# Parse the access token from the response
tokens = response.json()
access_token = tokens.get('access_token')  # Ensure token retrieval

# Check if the token is retrieved successfully
if not access_token:
    print("Error: Unable to retrieve access token.")
    exit()

# Define functions to interact with the Spotify API

def get_saved_albums():
    """Fetch the user's saved albums."""
    endpoint = 'https://api.spotify.com/v1/me/albums'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_liked_songs():
    """Fetch the user's liked songs."""
    endpoint = 'https://api.spotify.com/v1/me/tracks'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_playlists():
    """Fetch the user's playlists."""
    endpoint = 'https://api.spotify.com/v1/me/playlists'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(endpoint, headers=headers)
    return response.json()

# Fetch and display the user's data

# Display user's saved albums
saved_albums = get_saved_albums()
print("\nUser's Saved Albums:")
for album in saved_albums.get('items', []):
    album_name = album['album']['name']
    artists = ', '.join(artist['name'] for artist in album['album']['artists'])
    print(f" - {album_name} by {artists}")

# Display user's liked songs
liked_songs = get_liked_songs()
print("\nUser's Liked Songs:")
for song in liked_songs.get('items', []):
    song_name = song['track']['name']
    artists = ', '.join(artist['name'] for artist in song['track']['artists'])
    print(f" - {song_name} by {artists}")

# Display user's playlists
playlists = get_playlists()
print("\nUser's Playlists:")
for playlist in playlists.get('items', []):
    playlist_name = playlist['name']
    playlist_id = playlist['id']
    print(f" - {playlist_name} (ID: {playlist_id})")
