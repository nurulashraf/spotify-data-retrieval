import requests
import base64
import os
from datetime import datetime, timedelta

class SpotifyAuthManager:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        # Path to store tokens securely
        self.token_file = 'spotify_tokens.txt'

        # Load existing tokens
        self.load_tokens()

    def _get_auth_base64(self):
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode('utf-8')
        return base64.b64encode(auth_bytes).decode('utf-8')

    def _save_tokens(self, access_token, refresh_token, expires_at):
        with open(self.token_file, 'w') as f:
            f.write(f"{access_token}\n{refresh_token}\n{expires_at}")

    def load_tokens(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                lines = f.read().strip().split('\n')
                if len(lines) == 3:
                    self.access_token, self.refresh_token, expires_str = lines
                    self.expires_at = datetime.fromisoformat(expires_str)
                else:
                    self.access_token = self.refresh_token = None
                    self.expires_at = datetime.min
        else:
            self.access_token = self.refresh_token = None
            self.expires_at = datetime.min

    def get_authorization_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'user-library-read playlist-read-private user-read-private user-read-email'
        }
        return f"https://accounts.spotify.com/authorize?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    def exchange_code_for_token(self, auth_code):
        auth_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + self._get_auth_base64(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(auth_url, headers=headers, data=data)
        tokens = response.json()

        # Save tokens
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        expires_in = tokens.get('expires_in', 3600)  # Default to 1 hour if not specified
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        self._save_tokens(access_token, refresh_token, expires_at.isoformat())

        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

        return access_token, refresh_token

    def refresh_access_token(self):
        if not self.refresh_token:
            raise ValueError("No refresh token available. Please re-authenticate.")

        auth_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + self._get_auth_base64(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        response = requests.post(auth_url, headers=headers, data=data)
        tokens = response.json()

        # Update access token
        access_token = tokens['access_token']
        expires_in = tokens.get('expires_in', 3600)  # Default to 1 hour if not specified
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        # Save new access token
        self._save_tokens(access_token, self.refresh_token, expires_at.isoformat())

        self.access_token = access_token
        self.expires_at = expires_at

        return access_token

    def get_access_token(self):
        # Check if token is expired or about to expire (within 5 minutes)
        if (not self.access_token or
            datetime.now() >= self.expires_at - timedelta(minutes=5)):
            return self.refresh_access_token()

        return self.access_token

    def get_saved_albums(self):
        endpoint = 'https://api.spotify.com/v1/me/albums'
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}'
        }

        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_liked_songs(self):
        endpoint = 'https://api.spotify.com/v1/me/tracks'
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}'
        }

        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_playlists(self):
        endpoint = 'https://api.spotify.com/v1/me/playlists'
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}'
        }

        response = requests.get(endpoint, headers=headers)
        return response.json()


def main():
    # Insert Spotify credentials here
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    REDIRECT_URI = ''

    # Initialize Spotify Auth Manager
    spotify_auth = SpotifyAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    # First-time setup: If no tokens exist, you need to get an authorization code
    # Uncomment and follow these steps if it's your first time or tokens are invalid
    # 1. Print the authorization URL
    # print("Please visit this URL and authorize the app:")
    # print(spotify_auth.get_authorization_url())

    # 2. After authorization, replace with the actual authorization code
    # auth_code = ''
    # spotify_auth.exchange_code_for_token(auth_code)

    # Now you can fetch data
    saved_albums = spotify_auth.get_saved_albums()
    print("User's Saved Albums:")
    for album in saved_albums.get('items', []):
        print(f" - {album['album']['name']} by {', '.join(artist['name'] for artist in album['album']['artists'])}")

    liked_songs = spotify_auth.get_liked_songs()
    print("\nUser's Liked Songs:")
    for song in liked_songs.get('items', []):
        print(f" - {song['track']['name']} by {', '.join(artist['name'] for artist in song['track']['artists'])}")

    playlists = spotify_auth.get_playlists()
    print("\nUser's Playlists:")
    for playlist in playlists.get('items', []):
        print(f" - {playlist['name']} (ID: {playlist['id']})")

if __name__ == "__main__":
    main()
