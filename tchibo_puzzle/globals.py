import json
from pathlib import Path

RESOLUTION = WIDTH, HEIGHT = (750, 750)
ASSETS_PATH = Path("assets")
GAMES_PATH = Path("saved_games")
CAPTION = "Tchibo Game"
MIN_BALLS_TO_SAVE = 0.5
GAP = 0.06

# try loading settings from json file
try:
    with open("settings.json", "rb") as _file:
        _settings = json.load(_file)
        _res = _settings["display"]
        _paths = _settings["paths"]
        RESOLUTION = WIDTH, HEIGHT = _res["width"], _res["height"]
        ASSETS_PATH = Path(_paths["assets"])
        GAMES_PATH = Path(_paths["savedGames"])
        CAPTION = _settings["caption"]
        MIN_BALLS_TO_SAVE = _settings["minBallsToSave"]
        GAP = _settings["boardGap"]
except IOError:
    pass

# colors
WHITE = (255, 255, 255)
GRAY = tuple((int(n * 0.4) for n in WHITE))
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (10, 10, 255)
PINK = (255, 182, 193)

EMPTY_FIELD = "_"
FILLED_FIELD = "O"
