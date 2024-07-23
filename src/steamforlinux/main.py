# to run the server, use the following command:
# fastapi dev .\src\steamforlinux\main.py

from fastapi import FastAPI
import json
import pathlib
from services.webscraping import fetch_operating_system_requirements
from models import models


STEAM_API_RESPONSE = (
    pathlib.Path(__file__).parent.parent / "mocks/steamapi_response.json"
)

try:
    with open(STEAM_API_RESPONSE) as f:
        data = json.load(f)
        steam_api_response = models.SteamAPIResponse(**data)
except FileNotFoundError:
    raise FileNotFoundError("File not found")


app = FastAPI()


@app.get("/")
async def read_root():
    # return data['response']['games']
    games = steam_api_response.response.games
    response = []
    for game in games:
        data = fetch_operating_system_requirements(game.appid)
        response.append(data)
    return response
