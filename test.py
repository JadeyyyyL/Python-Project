import spotify_token
import nlp_mood
import pprint 
from requests import get
import json
import random

def get_header(token):
    """Returns a dictionary that contains the authorization header with the access token."""
    return {"Authorization": "Bearer " + token}

def search_artist_id(artist_name):
    """Returns the Spotify ID of an artist."""
    token = spotify_token.get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    params = {"q": artist_name, "type": "artist"}

    response_data = get(url, headers=headers, params=params)
    data = response_data.json()
    # pprint.pprint(data)
    data = data["artists"]["items"][0]
    # pprint.pprint(artist_data)
    return data["id"]

def get_related_artist(id):
    """Return the Top 5 related artist."""
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/artists/{id}/related-artists"
    headers = get_header(token)
    response_data = get(url, headers=headers)
    related_artists = response_data.json()["artists"]

    top_5 = [artist["name"] for artist in related_artists[:5]]
    return top_5

def search_track(track_name, artist_name, album_name=None, year=None, genre=None, market=None):
    token = spotify_token.get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    query = f"track:{track_name} artist:{artist_name}"
    params = {"q": query, "type": "track", "limit": 1 }
    response = get(url, headers=headers, params=params)
    response.raise_for_status()
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

def search_audio_features(track_id):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_header(token)
    response = get(url, headers=headers)
    data = response.json()
    pprint.pprint(data)
    # track_features = {
        # 'valence': data['valence']
    # }
    # return track_features

playlist = "Today's Top Hits"
playlist_id = search_playlist_id(playlist)
top_hits_tracks = get_playlist_tracks(playlist_id)
print(top_hits_tracks)
# test1 = search_audio_features(top_hits_tracks[0]["id"])
# print(test1)