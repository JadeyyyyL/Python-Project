import config
import requests

def get_token():
    """
    This function retrieves an access token from Spotify.

    Parameters:
    - client_id: The client ID for your Spotify application.
    - client_secret: The client secret for your Spotify application.

    Returns:
    - The access token as a string.
    """
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, data=data)
    json_response = response.json()
    # print(json_response)
    access_token = json_response["access_token"]
    return access_token

def main():
    print(get_token())

if __name__ == "__main__":
    main()