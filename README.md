# Spotify Data Retrieval Tools

A collection of Python scripts to interact with the Spotify Web API for retrieving user library data and artist information. This repository provides easy-to-use tools for accessing various Spotify data endpoints.

## Features

- User Library Data Retrieval:
  - Access saved albums
  - View liked songs
  - List user playlists
  
- Artist Data Retrieval:
  - Search for artists
  - Get artist's top tracks
  - Access artist's albums
  - View album tracks
  - Retrieve detailed artist information

## Prerequisites

- Python 3.6 or higher
- Spotify Developer account
- Spotify API credentials (Client ID and Client Secret)

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/spotify-data-retrieval.git
   cd spotify-data-retrieval
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a Spotify Developer account and register your application at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Usage

### Configuration

1. In the Spotify Developer Dashboard:
   - Create a new application
   - Get your Client ID and Client Secret
   - Set up your Redirect URI
   - Add the URI to your application settings

2. Update the credentials in the scripts:
   - Open `src/spotify_user_data_retrieval.ipynb`
   - Replace the placeholder values with your credentials:
     ```python
     client_id = 'your_client_id'
     client_secret = 'your_client_secret'
     redirect_uri = 'your_redirect_uri'
     ```
   - Do the same for `src/spotify_artist_data_retrieval.ipynb`

### Running the Scripts

1. For User Data Retrieval:
   - Open `src/spotify_user_data_retrieval.ipynb` in Jupyter Notebook or Google Colab
   - Run the first cell with authentication code
   - After running, a Spotify authorization page will open in your browser
   - Authorize the application
   - You will be redirected to your redirect URI
   - In the URL of the redirect page, look for the code parameter after `?code=`
   - Copy the code value (everything after `?code=` and before any `&` if present)
   - In the second cell of the notebook, replace the placeholder:
     ```python
     auth_code = 'your_authorization_code'  # Replace with the code from the URL
     ```
   - Run the remaining cells to fetch user data

2. For Artist Data Retrieval:
   - Open `src/spotify_artist_data_retrieval.ipynb`
   - In the second cell, locate the search query variable:
     ```python
     search_query = 'desired_artist_name'  # Replace with desired artist name
     ```
   - Replace the placeholder with your desired artist name (e.g., 'Taylor Swift', 'The Beatles')
   - The script will return:
     - List of matching artists (top 5 results)
     - Detailed information about the top match
     - Top tracks from the artist
     - Recent albums
     - Tracks from their most recent album
   - Run all cells to get the complete artist information

## Scopes Used

The following Spotify API scopes are used in this project:
- `user-library-read`: Access user's saved albums and tracks
- `user-top-read`: Access user's top artists and tracks
- `user-read-playback-state`: Read user's playback state

## Limitations
- Access token expires after a short period
- Requires manual token refresh

## Contributing
Contributions, issues, and feature requests are welcome!

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
