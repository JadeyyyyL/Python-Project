from requests import get
import spotify_token


def get_header(token):
    """
    Returns a dictionary that contains the authorization header with the access token.
    """
    return {"Authorization": "Bearer " + token}

def search_tracks(keyword, limit=50):
    token = spotify_token.get_token()
    url = f'https://api.spotify.com/v1/search?q={keyword}&type=track&limit={limit}'
    headers = get_header(token)
    response = get(url, headers=headers)
    if response.status_code == 200:
        tracks = response.json()['tracks']['items']
        return tracks
    else:
        print("Error:", response.status_code)
        return []

# Example usage
keyword = 'dance'
tracks = search_tracks(keyword)
for track in tracks:
    print("Name:", track['name'])
    print("Artist:", track['artists'][0]['name'])
    print("Album:", track['album']['name'])
    print("Listen on Spotify:", track['external_urls']['spotify'])
    print()