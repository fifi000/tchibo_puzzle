from pathlib import Path

RESOLUTION = WIDTH, HEIGHT = tuple(750 for _ in range(2))

# colors
WHITE = (255, 255, 255)
GRAY = tuple((int(n*0.4) for n in WHITE))
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (10, 10, 255)
PINK = (255, 182, 193)
COLORS = [GRAY]

# assets folder path
ASSETS_PATH = Path("assets")

# game save
GAMES_PATH = Path("saved_games")
EMPTY_FIELD = "_"
FILLED_FIELD = "O"


