import spotify_token
import pprint 
from requests import get
import json

def get_header(token):
    """
    Returns a dictionary that contains the authorization header with the access token.
    """
    return {"Authorization": "Bearer " + token}

def search_artist(artist_name):
    token = spotify_token.get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    params = {"q": artist_name, "type": "artist"}

    response_data = get(url, headers=headers, params=params)
    data = response_data.json()
    # pprint.pprint(data)
    data = data["artists"]["items"][0]
    # pprint.pprint(artist_data)
    return data

def get_artist_id(data):
    return data["id"] 

def get_related_artist(id):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/artists/{id}/related-artists"
    headers = get_header(token)
    response_data = get(url, headers=headers)
    related_artists = response_data.json()["artists"]

    top_5 = [artist["name"] for artist in related_artists[:5]]
    return top_5

def search_playlist(playlist_name):
    token = spotify_token.get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    params = {"q": playlist_name, "type": "playlist"}

    response_data = get(url, headers=headers, params=params)
    data = response_data.json()
    data = data["playlists"]["items"][0]
    # pprint.pprint(data)
    return data

def get_playlist_id(playlist_data):
    return playlist_data["id"]

def search_track_by_playlist(playlist_id, limit=100):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_header(token)

    response_data = get(url, headers=headers)
    data = response_data.json()
    # pprint.pprint(data)
    return data

def extract_track_names(data):
    tracks = []

    for item in data.get("items", []):
        track_names = item.get("track", {}).get("name")
        if track_names:
            tracks.append(track_names)
        else:
            print("no tracks found")
    return tracks
    # print(tracks)
    

def search_audio_feature(id):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/audio-features/{id}"    
    headers = get_header(token)
    # params = {"country": country}

    response_data = get(url, headers=headers)
    data = response_data.json()
    pprint.pprint(data)
    # return data
    

def main():
    artist = "BLACKPINK"
    artist_data = search_artist(artist)
    artist_id = get_artist_id(artist_data)
    # print(get_related_artist(artist_id))

    playlist = "Today's Top Hits"
    playlist_data = search_playlist(playlist)
    playlist_id = get_playlist_id(playlist_data)
    # print(playlist_id)
    song_data = search_track_by_playlist(playlist_id)
    # pprint.pprint(song_data)

    extract_track_names(song_data)

    

    
    # search_audio_feature(id)

    # print(top_track_data["tracks"])


if __name__ == "__main__":
    main()