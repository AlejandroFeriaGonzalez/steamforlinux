import os

import dotenv
import httpx

from ..models import models

dotenv.load_dotenv()
KEY = os.getenv("STEAM_API_KEY")


async def getOwnedGames(steamid: int) -> models.SteamAPIResponse:
    """
    Retrieves the list of owned games for a given Steam ID.

    Args:
        steamid (int): The Steam ID of the user.

    Returns:
        models.SteamAPIResponse: An instance of the SteamAPIResponse model class containing the response data.

    Raises:
        httpx.RequestError: If there is an error while making the HTTP request.
    """
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={KEY}&steamid={steamid}&format=json"

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            r.raise_for_status()
            return models.SteamAPIResponse(**r.json())
    except httpx.RequestError as e:
        raise e
    except httpx.HTTPStatusError as e:
        raise e


async def getGameInfo(appid: int) -> models.GameInfo:
    """
    Retrieves game information from the Steam API based on the provided appid.

    Args:
        appid (int): The unique identifier of the game on Steam.

    Returns:
        models.GameInfo: An instance of the GameInfo model containing the retrieved game information.

    Raises:
        httpx.RequestError: If there is an error while making the HTTP request to the Steam API.
    """
    print(f"Inicio {appid}")
    base_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(base_url)
            r.raise_for_status()
            response = r.json()[str(appid)]

            if response["success"]:
                data = response["data"]
                print(f"Fin {appid}")
                return models.GameInfo(**data)
            else:
                print(f"Game with appid {appid} not found")
                return models.GameInfo(
                    name="Not Found",
                    header_image="",
                    platforms=models.Platform(windows=False, mac=False, linux=False),
                )

    except httpx.RequestError as e:
        raise e
