import json
from time import sleep
import creds
from pprint import pp
from util import timeit


@timeit
def authenticate_spotify(client_id: str, client_secret: str, username: str, redirect_url: str, scope: str = "private"):
    """
    Creates a SpotifyAuth Object for Working with API.

    :param client_id: Spotify App Client ID
    :param client_secret: Spotify App Secret
    :param username: Spotify Username
    :param redirect_url: Redirect Link
    :param scope: Private/Public
    :return: SpotifyAuth Object
    """
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    sp_obj = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=f"playlist-modify-{scope}",
            redirect_uri=redirect_url,
            client_id=client_id,
            client_secret=client_secret,
            show_dialog=True,
            cache_path="token.json",
            username=username,
        )
    )

    return sp_obj


@timeit
def get_track_uri(sp_obj, song_list: list, limit_search: int = 1) -> list:
    """
    Gets URIs for List of Songs from Spotify.
    :param sp_obj: Spotify Auth Obj
    :param song_list: List of Songs
    :param limit_search: How Many Hit Searched to Return.
    :return: list of songs uri's
    """
    song_uri_list = []

    for song in song_list:
        sp = sp_obj
        result = sp.search(q=song, limit=limit_search)
        song_uri_list.append(result['tracks']['items'][0]['uri'])

    return song_uri_list


@timeit
def add_tracks_to_playlist(sp_obj, user_id: str, playlist_id: str, uri_list: list, ):
    """
    Adds Songs to a Playlist Based on Auth and PlaylistID.
    :param sp_obj: Spotify Auth
    :param user_id: UserID
    :param playlist_id: PlaylistID to Modify
    :param uri_list: List of URI's To Add
    :return: None
    """
    sp = sp_obj
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=uri_list)
    return sp


@timeit
def store_playlist(new_playlist: dict, playlist_storage_path: str) -> None:
    """
    Stores Name, ID and Href of the Playlist for Future Usage.
    :param new_playlist:
    :param playlist_storage_path:
    :return: JSON File with Playlist ID
    """
    playlist_dict = {
        'playlist_name': new_playlist['name'],
        'playlist_id': new_playlist['id'],
        'playlist_href': new_playlist['href']
    }

    try:
        with open(playlist_storage_path, 'r+') as storage:
            print("FileWorker: Trying to Read File.")
            playlists = json.load(storage)
            # pp(playlists)

    except:
        print("FileWorker: Issue Reading File. Adding New Playlist Information.")
        with open(playlist_storage_path, 'a+') as storage:
            storage.write(json.dumps([playlist_dict], indent=4))

    else:
        print("FileWorker: No Exception Found: Appending New Playlist.")
        with open(playlist_storage_path, 'w') as storage:
            playlists.append(playlist_dict)
            storage.write(json.dumps(playlists, indent=4))


@timeit
def delete_playlist(client_id: str, client_secret: str, username: str, redirect_url: str,
                    playlist_storage_path: str):
    """
    Deletes The Selected Playlist from Spotify.
    :param client_id: Spotify App Client ID
    :param client_secret: Spotify App Secret
    :param username: Spotify Username
    :param redirect_url: Redirect Link
    :param playlist_storage_path: Path to Read Playlist Information
    :return: None
    """
    sp_obj = authenticate_spotify(client_id, client_secret, username, redirect_url)
    with open(playlist_storage_path, 'r') as playlist_data:
        data = json.load(playlist_data)
        pp(data)
        playlist_id = input("What Playlist to Delete? ID Only ")

    # Find and remove the playlist with that ID
    filtered_data = [playlist for playlist in data if playlist_id not in playlist.values()]
    # pp(filtered_data)
    # Save the updated data back to the file
    with open(playlist_storage_path, 'w') as playlist_data:
        json.dump(filtered_data, playlist_data, indent=4)

    print(f"Playlist with ID {playlist_id} deleted successfully.")

    sp_obj.current_user_unfollow_playlist(playlist_id=playlist_id)




@timeit
def main():
    """
    This is a Main Function to Test spotify_api.py.
    :return: None
    """
    print("-------------------- TEST...TEST...TEST --------------------")
    print("Running Directly from File.")
    sp_obj = authenticate_spotify(creds.CLIENT_ID, creds.CLIENT_SECRET, creds.USERNAME, redirect_url=creds.REDIRECT_URL)
    user_info = sp_obj.current_user()

    # TEST: Printing UserID
    print("-----> TEST: Printing UserID")
    print(user_info['id'])

    # TEST: Capture List of Song URI
    print("-----> TEST: Printing 3 Song URI")
    test_songs = ['Candy Shop', 'Boulevard Of Broken Dreams', 'Let Me Love You']
    song_uri_list = get_track_uri(sp_obj=sp_obj, song_list=test_songs)
    pp(song_uri_list)

    # TEST: Create New Custom Playlist
    print("-----> TEST: Creating a New Custom Playlist Called:")
    my_playlist = sp_obj.user_playlist_create(user=user_info['id'],
                                              name='TestSpotifyAPI v2', description='Testing API', public=False)
    # pp(my_playlist)
    sp_obj.playlist_add_items(playlist_id=my_playlist['id'], items=song_uri_list)

    # TEST: Store New Playlist Info in JSON File
    print("-----> TEST: Storing Playlist Info to test_playlist_storage.json")
    store_playlist(my_playlist, playlist_storage_path='test_playlist_storage.json')

    # TEST: Delete Spotify Test Playlist
    print("-----> TEST: Deleting Test Playlist from Spotify")
    print("-----> TEST: Timer 10secs")
    sleep(10)
    print("-----> TEST: Deleted Test Playlist")
    sp_obj.current_user_unfollow_playlist(playlist_id=my_playlist['id'])


if __name__ == '__main__':
    main()
