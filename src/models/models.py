from pydantic import BaseModel


class Game(BaseModel):
    appid: int
    # playtime_forever: int
    # playtime_windows_forever: int
    # playtime_mac_forever: int
    # playtime_linux_forever: int
    # playtime_deck_forever: int
    # rtime_last_played: int
    # playtime_disconnected: int


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
