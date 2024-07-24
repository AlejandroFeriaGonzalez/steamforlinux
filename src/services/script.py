import requests
from pydantic import BaseModel

class Platform(BaseModel):
    windows: bool
    mac: bool
    linux: bool

class GameInfo(BaseModel):
    name: str
    header_image: str
    platforms: Platform


def getGameInfo(appid: int):
    base_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

    try:
        r = requests.get(base_url)
        r.raise_for_status()
        data = r.json()[str(appid)]["data"]
        return GameInfo(**data)

    except requests.exceptions.RequestException as e:
        raise e

print(getGameInfo(945360))