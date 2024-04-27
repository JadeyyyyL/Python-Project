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

def artist_id(data):
    return data["id"] 

# def artist_name(data):
#     return data["name"]

# def artist_followers(data):
#     return data["followers"]["total"]

# def genre(data):
#     return data["genres"]

def get_related_artist(id):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/artists/{id}/related-artists"
    headers = get_header(token)
    response_data = get(url, headers=headers)
    related_artists = response_data.json()["artists"]

    top_5 = [artist["name"] for artist in related_artists[:5]]
    return top_5

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
    id = artist_id(artist_data)

    print(get_related_artist(id))

    # pprint.pprint(artist_data)

    # get_songs_by_artist(artist)
    
    # search_audio_feature(id)

    # print(top_track_data["tracks"])


    # search_artist(artist_name)
    # 41MozSoPIsD1dJM0CLPjZF

    # print(artist_id(artist_data))
    # print(artist_name(artist_data))
    # print(artist_followers(artist_data))
    # print(genre(artist_data))

if __name__ == "__main__":
    main()