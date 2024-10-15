# python -m src.main

import asyncio
import os
import pathlib

import dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .services.steamApi import getGameInfo, getOwnedGames, httpx

dotenv.load_dotenv()
MODE = os.getenv("MODE")

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

app.mount("/static", StaticFiles(directory=SRC / "templates"), name="static")
templates = Jinja2Templates(directory=SRC / "templates/")


@app.middleware("http")
async def https_redirect(request: Request, call_next):
    print(MODE)
    if MODE == "production" and request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url)
    response = await call_next(request)
    return response


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
