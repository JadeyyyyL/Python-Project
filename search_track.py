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

def search_playlist_id(playlist_name):
    """Returns the Spotify ID of a playlist."""
    token = spotify_token.get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    params = {"q": playlist_name, "type": "playlist"}

    response_data = get(url, headers=headers, params=params)
    data = response_data.json()
    data = data["playlists"]["items"][0]
    # pprint.pprint(data)
    return data["id"]

top_hits_playlist_id = search_playlist_id("Today's Top Hits")

print("Spotify ID for Top Hits playlist:", top_hits_playlist_id)
    
def get_playlist_tracks(playlist_id):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_header(token)
    params = {"limit": 100}
    tracks = []

    
    response = get(url, headers=headers, params=params)
    data = response.json()
    items = data["items"]
    for item in items:
        track = item['track']
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name']
        }
        tracks.append(track_info)

    if data['next']:
        url = data['next']

    return tracks

# Get tracks from Spotify's "Top Hits" playlist
top_hits_tracks = get_playlist_tracks(top_hits_playlist_id)

for idx, track in enumerate(top_hits_tracks, start=1):
   print(f"{idx}. {track['name']} - {track['artist']}")
   
def search_audio_features(track_id):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_header(token)
    response = get(url, headers=headers)
    data = response.json()
    track_features = {
        'valence': data['valence']
    }
    return track_features

test1 = search_audio_features(top_hits_tracks[0]["id"])
# print(test1)

def get_top_hits_features(top_hits_tracks):
    top_hits_features = []  
    for track in top_hits_tracks:
        basic_info = search_track(track['name'], track['artist'])  
        name = basic_info['name']
        artist = basic_info['artist']
        album = basic_info['album']
        preview_url = basic_info['preview_url']
        spotify_url = basic_info['spotify_url']
            
        audio_features = search_audio_features(track['id'])   
        track_info = {
        'name': name,
        'artist': artist,
        'album': album,
        'preview_url': preview_url,
        'spotify_url': spotify_url,
        'audio_features': audio_features  
        }
            
        top_hits_features.append(track_info)
    return top_hits_features

test2 = get_top_hits_features(top_hits_tracks)
print(test2[0])
