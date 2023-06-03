import requests
import config

async def get_player_stats(username):
    headers = {"TRN-Api-Key": config.TRACKER_API_KEY}
    url = f"https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{username}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            player_stats = data["data"]["segments"][0]["stats"]
            print(f"Data: {data}")
            print(f"Player stats: {player_stats}")
            return player_stats
        except:
            print(f"Unable to retrieve player stats.")
            return None
    elif response.status_code == 401:
        print(f"Unauthorized access. Please check your API key.")
        return None
    else:
        print(f"Error {response.status_code}")
        return None