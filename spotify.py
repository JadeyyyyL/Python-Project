import config, spotify_token

def get_header(token):
    return {"Authorization": "Bearer" + token}

def get_artist():
    url = "https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myaseg"
    headers = {""}

def main():
    token = spotify_token.get_token()

if __name__ == "__main__":
    main()