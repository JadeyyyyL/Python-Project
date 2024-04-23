import spotify_token
import pprint 
from requests import get

def get_header(token):
    """
    Returns a dictionary that contains the authorization header with the access token.
    """
    return {"Authorization": "Bearer " + token}

def search_track(track_name, artist_name):
    token = spotify_token.get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_header(token)
    query = f"{track_name} artist:{artist_name}"
    params = {"q": query, "type": "track"}

    response_data = get(url, headers=headers, params=params)
    data = response_data.json()
    pprint.pprint(data)
    # data = data["artists"]["items"][0]
    # pprint.pprint(artist_data)
    # return data

search_track("YES or YES", "TWICE")