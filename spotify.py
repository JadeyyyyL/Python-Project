import spotify_token
import pprint 
from requests import get

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
    artist_data = data["artists"]["items"][0]
    # pprint.pprint(artist_data)
    return artist_data

def artist_id(data):
    return data["id"] 

def artist_name(data):
    return data["name"]

def artist_followers(data):
    return data["followers"]["total"]

def genre(data):
    return data["genres"]

def search_top_track(id, country="US"):
    token = spotify_token.get_token()
    url = f"https://api.spotify.com/v1/artists/{id}/top-tracks"    
    headers = get_header(token)
    params = {"country": country}

    response_data = get(url, headers=headers, params=params)
    data = response_data.json()
    pprint.pprint(data)



def main():
    artist = "BLACKPINK"
    data = search_artist(artist)
    id = artist_id(data)

    # search_artist(artist_name)
    # 41MozSoPIsD1dJM0CLPjZF

    print(artist_id(data))
    print(artist_name(data))
    print(artist_followers(data))
    print(genre(data))

    search_top_track(id)

if __name__ == "__main__":
    main()