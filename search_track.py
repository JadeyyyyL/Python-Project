import spotify_token
import pprint 
from requests import get

def get_header(token):
    """
    Returns a dictionary that contains the authorization header with the access token.
    """
    return {"Authorization": "Bearer " + token}

def search_track(track_name, artist_name, album_name=None, year=None, genre=None, market=None):
    token = spotify_token.get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    query = f"track:{track_name} artist:{artist_name}"
 

# search_track("Greedy", "Tate McRae", album_name="THINK LATER")
search_track("Standing Next to You", "Jungkook")