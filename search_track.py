import spotify_token
import pprint 
from requests import get

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
    if album_name:
        query += f" album:{album_name}"
    if year:
        query += f" year:{year}"
    if genre:
        query += f" genre:{genre}"
    if market:
        query += f" market:{market}"
        
    params = {"q": query, "type": "track"}
    response_data = get(url, headers=headers, params=params)
    data = response_data.json()
    track_ids = [item['id'] for item in data['tracks']['items']]
    # print(track_ids[0])
    # pprint.pprint(data)
    return track_ids[0]

search_track("Greedy", "Tate McRae", album_name="THINK LATER")