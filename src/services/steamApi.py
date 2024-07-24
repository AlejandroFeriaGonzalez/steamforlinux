import os
import requests
from models import models
import dotenv

dotenv.load_dotenv()
KEY = os.getenv("STEAM_API_KEY")


def getOwnedGames(steamid: int) -> models.SteamAPIResponse:
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={KEY}&steamid={steamid}&format=json"

    try:
        r = requests.get(url)
        r.raise_for_status()
        return models.SteamAPIResponse(**r.json())
    except requests.exceptions.RequestException as e:
        raise e


def getGameInfo(appid: int):
    base_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

    try:
        r = requests.get(base_url)
        r.raise_for_status()
        response = r.json()[str(appid)]

        if response["success"]:
            data = response["data"]
            return models.GameInfo(**data)
        else:
            print(f"Game with appid {appid} not found")
            return models.GameInfo(
                name="Not Found",
                header_image="",
                platforms=models.Platform(windows=False, mac=False, linux=False),
            )

    except requests.exceptions.RequestException as e:
        raise e
