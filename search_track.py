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
    params = {
        "q": query,
        "type": "track",
        "limit": 1 
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    tracks = data.get('tracks', {}).get('items', [])
    if tracks:
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
#print(search_track("Standing Next to You", "Jung Kook"))

def get_top_hits_playlist_id(playlist_name):
    token = spotify_token.get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    query = f"playlist:{playlist_name}"
    params = {
        "q": query,
        "type": "playlist",
        "limit": 1 
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    playlists = data.get('playlists', {}).get('items', [])
    if playlists:
        playlist_id = playlists[0]['id']
        return playlist_id
    else:
        return None

top_hits_playlist_id = get_top_hits_playlist_id("Today's Top Hits")

print("Spotify ID for Top Hits playlist:", top_hits_playlist_id)
    
def get_playlist_tracks(playlist_id):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_header(token)
    params = {
        "limit": 100 
    }
    tracks = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        items = data.get('items', [])
        for item in items:
            track = item['track']
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name']
            }
            tracks.append(track_info)

        if data['next']:
            url = data['next']
        else:
            break

    return tracks

# Example usage: Get tracks from Spotify's "Top Hits" playlist
top_hits_tracks = get_playlist_tracks(top_hits_playlist_id)

for idx, track in enumerate(top_hits_tracks, start=1):
   print(f"{idx}. {track['name']} - {track['artist']}")
   
