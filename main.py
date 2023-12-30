import spotify_api
import billboard_scraper
import creds
import date_format

# ------------------------------------ BILLBOARD SCRAPE CODE ------------------------------------
# date = '2005-03-05'
date = input("What Date do you want the Top 100 Songs from? YYYY-MM-DD ").strip()
# ............ Format User Date
print("PROD---> Validate User Date Input")
checked_date = billboard_scraper.validate_date(date)

# ............ Scrape Billboards Top 100 for User Date
print("PROD---> Get Billboard Top 100 Information")
chart = billboard_scraper.get_billboard100(checked_date)

# ------------------------------------ SPOTIFY_API CODE ------------------------------------

# ............ Create SpotifyAuth Object
print("PROD---> Creating SpotifyAuth Object")
sp = spotify_api.authenticate_spotify(creds.CLIENT_ID, creds.CLIENT_SECRET,
                                      creds.USERNAME, redirect_url=creds.REDIRECT_URL)

# ............ Get User ID
print("PROD---> Fetching UserID")
user_info = sp.current_user()

# ............ Get URI for Each Song from Billboards Top 100
print("PROD---> Fetching Song URI's")
# <Could Be Improved With Speed Here>
song_uri_list = spotify_api.get_track_uri(sp, chart)

# ............ Playlist Information
title_date = date_format.format_date_MM_YYYY(date)
des = f"Playlist Created via Python App. Contains Billboards Top Songs from {title_date}. Enjoy!"

# ............ Create Custom Billboard Playlist
print("PROD---> Creating Playlist")
my_playlist = sp.user_playlist_create(user=user_info['id'],
                                      name=f'{title_date} BillBoard Top 100',
                                      description=des, public=False)

# ............ Store Playlist information
print("PROD---> Storing Playlist")
spotify_api.store_playlist(my_playlist, playlist_storage_path='playlist_storage.json')

# ............ Add Songs to Playlist
print("PROD---> Adding Songs to Playlist")
sp.playlist_add_items(playlist_id=my_playlist['id'], items=song_uri_list)
