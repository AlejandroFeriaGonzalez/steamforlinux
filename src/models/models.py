from pydantic import BaseModel


class Game(BaseModel):
    appid: int


class Response(BaseModel):
    games: list[Game]


class SteamAPIResponse(BaseModel):
    response: Response


class GameRequirements(BaseModel):
    game_title: str
    os_requirements: list[str]


class Platform(BaseModel):
    windows: bool
    mac: bool
    linux: bool


class GameInfo(BaseModel):
    name: str
    header_image: str
    platforms: Platform
