from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import models
from .services.steamApi import getGameInfo, getOwnedGames, httpx

import pathlib

SRC = pathlib.Path(__file__).parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=SRC / "templates"), name="static")
templates = Jinja2Templates(directory=SRC / "templates/")

@app.get("/")
async def root():
    return RedirectResponse(url="/index")

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/get_games/", response_class=HTMLResponse)
async def get_games(request: Request, steamid: int):
    try:
        data = await getOwnedGames(steamid)
        games: list[models.GameInfo] = []

        for game in data.response.games:
            game_info = await getGameInfo(game.appid)
            games.append(game_info)
        return templates.TemplateResponse(
            request, "responseList.html", {"games": games}
        )
    except httpx.RequestError as e:
        return templates.TemplateResponse(request, "error.html", {"error": str(e)})

@app.get("/game/")
async def read_game(appid: int):
    try:
        return await getGameInfo(appid)
    except httpx.RequestError as e:
        return {"error": str(e)}