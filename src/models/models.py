from pydantic import BaseModel

# http://api.steampowered.com/IPlayerService/GetOwnedGames

class Game(BaseModel):
    appid: int
    playtime_forever: int
    playtime_2weeks: int | None = None

class Response(BaseModel):
    game_count: int
    games: list[Game]



class SteamAPIResponse(BaseModel):
    response: Response

# https://store.steampowered.com/api/appdetails?appids={appid}


class Platform(BaseModel):
    windows: bool
    mac: bool
    linux: bool


class GameInfo(BaseModel):
    name: str
    header_image: str
    platforms: Platform

class GameCollection(BaseModel):
    games: list[GameInfo]