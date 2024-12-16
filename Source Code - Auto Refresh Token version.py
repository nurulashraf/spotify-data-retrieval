import requests
import base64
import os
from datetime import datetime, timedelta

class SpotifyAuthManager:
    """Manages Spotify API Authentication, including token exchange and refresh."""

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        # File to securely store access and refresh tokens
        self.token_file = 'spotify_tokens.txt'

        # Load existing tokens if available
        self.load_tokens()

    def _get_auth_base64(self):
        """Encodes client credentials in Base64 for API requests."""
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode('utf-8')
        return base64.b64encode(auth_bytes).decode('utf-8')

    def _save_tokens(self, access_token, refresh_token, expires_at):
        """Saves tokens and expiry details to a file."""
        with open(self.token_file, 'w') as f:
            f.write(f"{access_token}\n{refresh_token}\n{expires_at}")

    def load_tokens(self):
        """Loads tokens and expiry details from the token file."""
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
        """Generates the Spotify authorization URL for first-time authentication."""
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'user-library-read playlist-read-private user-read-private user-read-email'
        }
        return f"https://accounts.spotify.com/authorize?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    def exchange_code_for_token(self, auth_code):
        """Exchanges an authorization code for access and refresh tokens."""
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

        # Extract and save tokens
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        expires_in = tokens.get('expires_in', 3600)  # Default expiry time: 1 hour
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        self._save_tokens(access_token, refresh_token, expires_at.isoformat())
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

        return access_token, refresh_token

    def refresh_access_token(self):
        """Refreshes the access token using the stored refresh token."""
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

        # Update and save new access token
        access_token = tokens['access_token']
        expires_in = tokens.get('expires_in', 3600)
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        self._save_tokens(access_token, self.refresh_token, expires_at.isoformat())
        self.access_token = access_token
        self.expires_at = expires_at

        return access_token

    def get_access_token(self):
        """Returns a valid access token, refreshing it if necessary."""
        if not self.access_token or datetime.now() >= self.expires_at - timedelta(minutes=5):
            return self.refresh_access_token()
        return self.access_token

    # API Request Functions

    def get_saved_albums(self):
        """Fetches the user's saved albums from Spotify."""
        endpoint = 'https://api.spotify.com/v1/me/albums'
        headers = {'Authorization': f'Bearer {self.get_access_token()}'}
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_liked_songs(self):
        """Fetches the user's liked songs from Spotify."""
        endpoint = 'https://api.spotify.com/v1/me/tracks'
        headers = {'Authorization': f'Bearer {self.get_access_token()}'}
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_playlists(self):
        """Fetches the user's playlists from Spotify."""
        endpoint = 'https://api.spotify.com/v1/me/playlists'
        headers = {'Authorization': f'Bearer {self.get_access_token()}'}
        response = requests.get(endpoint, headers=headers)
        return response.json()


def main():
    """Main function to demonstrate the Spotify Auth Manager functionality."""
    # Spotify API credentials - Replace with your own
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    REDIRECT_URI = ''

    # Initialize the Spotify authentication manager
    spotify_auth = SpotifyAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    # First-time setup (uncomment if running for the first time)
    # print("Please visit this URL and authorize the app:")
    # print(spotify_auth.get_authorization_url())
    # auth_code = ''  # Replace with the authorization code
    # spotify_auth.exchange_code_for_token(auth_code)

    # Fetch and display user data
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
