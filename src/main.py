# python -m src.main

import asyncio
import json
import pathlib

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import models
import pydantic
from .services.steamApi import getGameInfo, getOwnedGames, httpx

SRC = pathlib.Path(__file__).parent

app = FastAPI(
    title="Steam For Linux",
    description="An API to retrieve information about Steam games and owned games for a given user.",
    version="0.1",
    summary="Steam Game Info API",
    terms_of_service="http://example.com/terms/",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    contact={
        "name": "Alejandro Feria Gonzalez",
        "url": "https://github.com/AlejandroFeriaGonzalez",
        "email": "alejandroferiagonzalez@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto para más seguridad en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=SRC / "static"), name="static")
templates = Jinja2Templates(directory=SRC / "static/")


@app.get("/")
async def root():
    return RedirectResponse(url="/index")


@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get(
    "/get_games/", response_class=JSONResponse, response_model=models.GameCollection
)
async def get_games(request: Request, steamid: int):
    try:
        data = await getOwnedGames(steamid)
        game_ids = [game.appid for game in data.response.games]

        games = await asyncio.gather(*[getGameInfo(appid) for appid in game_ids])

        return {"games": games}

    except httpx.RequestError as e:
        return {"httpx.RequestError": str(e)}
    except httpx.HTTPStatusError as e:
        return {"httpx.HTTPStatusError": str(e)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/render_owned_games/", response_class=HTMLResponse)
async def render_owned_games(request: Request, steamid: int):
    try:
        data = await getOwnedGames(steamid)
        game_ids = [game.appid for game in data.response.games]

        games = await asyncio.gather(*[getGameInfo(appid) for appid in game_ids])

        return templates.TemplateResponse(
            request, "responseList.html", {"games": games}
        )

    except httpx.RequestError as e:
        return templates.TemplateResponse(request, "error.html", {"error": str(e)})
    except httpx.HTTPStatusError as e:
        return templates.TemplateResponse(request, "error.html", {"error": str(e)})


@app.get("/game/")
async def read_game(appid: int):
    try:
        return await getGameInfo(appid)
    except httpx.RequestError as e:
        return {"error": str(e)}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.get("/mock", response_class=JSONResponse)
def test():
    try:
        json_path = pathlib.Path(__file__).parent / "mocks" / "games.json"
        with open(json_path, "r") as f:
            games_data = json.load(f)
        return games_data
    except FileNotFoundError:
        return JSONResponse(
            status_code=404, content={"error": "Games data file not found"}
        )


@app.get("/render_mock")
async def render_mock(request: Request):
    try:
        json_path = pathlib.Path(__file__).parent / "mocks" / "games.json"
        with open(json_path, "r") as f:
            games_data = json.load(f)
            games: list[models.GameInfo] = games_data["games"]
        return templates.TemplateResponse(
            request, "responseList.html", {"games": games}
        )
    except FileNotFoundError:
        return templates.TemplateResponse(
            request, "error.html", {"error": "Games data file not found"}
        )
