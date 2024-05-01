import spotify_token
import pprint 
from requests import get
import json

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

def search_track_by_playlist(playlist_id, limit=100):
    """Return a list of dictionaries of track info for the first 100 tracks from a playlist."""
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_header(token)

    tracks = []

    response_data = get(url, headers=headers)
    data = response_data.json()
    # pprint.pprint(data)

    items = data["items"]
    for item in items:
        track = item["track"]
        track_info = {
            "id": track["id"],
            "name": track["name"],
            "artist": track["artists"][0]["name"]
        }
        tracks.append(track_info)
    return tracks
  

def main():
    artist = "BLACKPINK"
    artist_id = search_artist_id(artist)
    print(get_related_artist(artist_id))

    playlist = "Today's Top Hits"
    playlist_id = search_playlist_id(playlist)
    print(playlist_id)
    song_data = search_track_by_playlist(playlist_id)
    #pprint.pprint(song_data)


if __name__ == "__main__":
    main()