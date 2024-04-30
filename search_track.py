import spotify_token
import pprint 
from requests import get
import requests

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
    params = {"q": query, "type": "track", "limit": 1 }
    response = get(url, headers=headers, params=params)
    data = response.json()
    tracks = data.get('tracks', {}).get('items', [])
    if tracks:
        # Extract relevant information from the first track found
        track_info = {
            "name": tracks[0]["name"],
            "artist": tracks[0]["artists"][0]["name"],
            "album": tracks[0]["album"]["name"],
            "preview_url": tracks[0]["preview_url"],
            "spotify_url": tracks[0]["external_urls"]["spotify"]
        }
        return track_info
    else:
        return "Track not found. Please check the track name and artist name."
    
# search_track("Greedy", "Tate McRae", album_name="THINK LATER")
print(search_track("Standing Next to You", "Jung Kook"))