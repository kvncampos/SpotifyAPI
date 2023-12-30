import creds
import spotify_api

spotify_api.delete_playlist(creds.CLIENT_ID, creds.CLIENT_SECRET,
                            creds.USERNAME, creds.REDIRECT_URL, 'playlist_storage.json')
