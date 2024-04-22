import spotify_token
import pprint 
from requests import get


def get_header(token):
    """
    Returns a dictionary that contains the authorization header with the access token.
    """
    return {"Authorization": "Bearer " + token}

def get_artist_id(token):
    url = "https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myaseg"
    headers = get_header(token)
    response_data = get(url, headers = headers)
    json_response_data = response_data.json()
    # pprint.pprint(json_response_data)
    return json_response_data["id"]


def main():
    token = spotify_token.get_token()
    # print(token)

    get_artist_id(token)

if __name__ == "__main__":
    main()