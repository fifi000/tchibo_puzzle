import pygame as pg

from globals import *
from structures.button import Button
from structures.container import HorizontalContainer


def get_text(text: str):
    return pg.font.SysFont("consolas", 24).render(text, True, WHITE)


class NavigationBar(HorizontalContainer):
    def __init__(self, game, pos=(0, 0), size=RESOLUTION):
        super(NavigationBar, self).__init__(pos, size)

        self.game = game
        self.folder_path = ASSETS_PATH / "nav_bar_emojis"

        self.gap = 50

        self.button_images = None
        self.set_images()

    @property
    def button_size(self):
        return self.height, self.height

    @property
    def switch_img_name(self):
        img = "switch_on.png" if self.game.puzzle_mode else "switch_off.png"
        return self.folder_path / img

    def init_buttons(self):
        board = self.game.board

        left_arrow_btn = Button(img_name=self.folder_path / "left_arrow.png", action=board.undo_move)
        right_arrow_btn = Button(img_name=self.folder_path / "right_arrow.png", action=board.redo_move)
        puzzle_btn = Button(img_name=self.folder_path / "puzzle.png", action=self.game.set_puzzle_mode)
        rush_btn = Button(img_name=self.folder_path / "fire.png", action=self.game.start_rush_mode)
        restart_btn = Button(img_name=self.folder_path / "restart.png", action=self.game.new_game)

        # left
        self.add_item(left_arrow_btn)
        self.add_item(right_arrow_btn)
        self.add_item(puzzle_btn)
        self.add_item(rush_btn)
        self.add_item(restart_btn)

    def set_images(self):
        self.button_images = {
            path: self.game.get_texture(path, self.button_size, True)
            for path in
            (list(self.button_images.keys()) if self.button_images else (ASSETS_PATH / "nav_bar_emojis").glob("*.png"))
        }

    def draw(self):
        self.draw_center()
