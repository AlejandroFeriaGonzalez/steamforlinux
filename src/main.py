# to run the server, use the following command:
# fastapi dev .\src\main.py

import json
import pathlib

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import models
from .services.steamApi import getGameInfo, getOwnedGames, requests

SRC = pathlib.Path(__file__).parent


STEAM_API_RESPONSE = SRC / "mocks/steamapi_response.json"

try:
    with open(STEAM_API_RESPONSE) as f:
        data = json.load(f)
        steam_api_response = models.SteamAPIResponse(**data)
except FileNotFoundError:
    raise FileNotFoundError("File not found")


app = FastAPI()
app.mount("/static", StaticFiles(directory=SRC / "templates"), name="static")
templates = Jinja2Templates(directory=SRC / "templates/")

# @app.get("/")
# async def read_root():
#     # return data['response']['games']
#     games = steam_api_response.response.games
#     response = []
#     for game in games:
#         data = fetch_operating_system_requirements(game.appid)
#         response.append(data)
#     return response


@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/get_games/", response_class=HTMLResponse)
async def get_games(request: Request, steamid: int):
    try:
        data = getOwnedGames(steamid)
        games: list[models.GameInfo] = []

        for game in data.response.games:
            game_info = getGameInfo(game.appid)
            games.append(game_info)
        return templates.TemplateResponse(
            request, "responseList.html", {"games": games}
        )
    except requests.exceptions.RequestException as e:
        return templates.TemplateResponse(request, "error.html", {"error": str(e)})


@app.get("/game/")
def read_game(appid: int):
    try:
        return getGameInfo(appid)
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
