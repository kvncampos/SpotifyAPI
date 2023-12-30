# Billboard Top 100 Playlist Generator

This simple Python script generates a Spotify playlist with the Top 100 songs from Billboard on a specified date.
Prerequisites

### Make sure you have the following installed:

    Python
    Spotify Developer credentials (Client ID, Client Secret, Redirect URL)
    Billboard API credentials (if applicable)

# Installation

### Clone this repository:

```bash
git clone https://github.com/your-username/billboard-spotify-playlist.git
```
### Install required Python packages:

```bash
pip install -r requirements.txt
```
### Set up your credentials:
    - Add your Spotify Developer credentials to creds.py.
    - If using the Billboard API, add your credentials to creds.py.

# Usage

    Run the script:

```bash
python main.py
```
    - Enter the date in the format YYYY-MM-DD when prompted.

    - The script will fetch the Top 100 songs from Billboard on the specified date, create a Spotify playlist, and add the songs to the playlist.

# Notes

    The playlist is not set as public by default.
    Playlist details are stored in playlist_storage.json.

### Enjoy your personalized Billboard Top 100 playlist!
