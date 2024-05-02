import spotify_token
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
    #print("Response status code:", response.status_code)
    data = response.json()
    print("Response status code:", response.status_code)
    #print("Response data:", data)
    track_features = {
        'valence': data['valence']
    }
    return track_features

def get_top_hits_features(top_hits_tracks):
    top_hits_features = []  
    for track in top_hits_tracks:
        basic_info = search_track(track['name'], track['artist'])  
        name = basic_info['name']
        artist = basic_info['artist']
        album = basic_info['album']
        preview_url = basic_info['preview_url']
        spotify_url = basic_info['spotify_url']
             
        valence = search_audio_features(track['id'])    
        track_info = {
        'name': name,
        'artist': artist,
        'album': album,
        'preview_url': preview_url,
        'spotify_url': spotify_url,
        'audio_features': valence  
        }
            
        top_hits_features.append(track_info)
    return top_hits_features

def categorize_songs_by_emotion(songs):
    categories = {
        "happy": (0.5, 1),
        "sad": (0, 0.5),
        "bored": (0.25, 0.75),
        "excited": (0.75, 1),
        "depressed": (0, 0.3),
        "anxious": (0.3, 0.5),
        "angry": (0.6, 0.8),
        "calm": (0.3, 0.6)
    }
    categorized_songs = {category: [] for category in categories}
    for song in songs:
        valence = song.get('audio_features', {}).get('valence', 0.5)
        if valence is not None:
            valence = float(valence)
            for category, (min_valence, max_valence) in categories.items():
                if min_valence is not None and max_valence is not None:
                    if min_valence <= valence <= max_valence:
                        categorized_songs[category].append(song)
    
    return categorized_songs

def main():
    artist = "BLACKPINK"
    artist_id = search_artist_id(artist)
    #print(get_related_artist(artist_id))
    #print()
    playlist = "Today's Top Hits"
    playlist_id = search_playlist_id(playlist)
    #print("Spotify ID for Top Hits playlist:", playlist_id)
    #print()
    top_hits_tracks = get_playlist_tracks(playlist_id)
    #for idx, track in enumerate(top_hits_tracks, start=1):
        #print(f"{idx}. {track['name']} - {track['artist']}")
    
    test1 = search_audio_features(top_hits_tracks[0]["id"])
    print(test1)
    test2 = get_top_hits_features(top_hits_tracks)
    # print(test2[0])
    for track in top_hits_tracks:
        track['audio_features'] = search_audio_features(track['id'])

    categorized_songs = categorize_songs_by_emotion(top_hits_tracks)

    for category, songs_in_category in categorized_songs.items():
        print(f"{category.capitalize()} Songs:")
        for song in songs_in_category:
            print(f"- {song['name']} by {song['artist']}")
        print()

if __name__ == "__main__":
    main()