import pygame as pg

from container import HorizontalContainer
from globals import *
from structures.button import Button


def get_text(text: str):
    return pg.font.SysFont("consolas", 24).render(text, True, WHITE)


class NavigationBar(HorizontalContainer):
    def __init__(self, game, pos=(0, 0), size=RESOLUTION):
        super(NavigationBar, self).__init__(pos, size)

        self.game = game
        self.folder_path = ASSETS_PATH / "nav_bar_emojis"

        self.gap = 30

        self.button_images = None
        self.set_images()

    @property
    def button_size(self):
        return self.height, self.height

    @property
    def switch_img_name(self):
        img = "switch_on.png" if self.game.challenge_mode else "switch_off.png"
        return self.folder_path / img

    def init_buttons(self):
        board = self.game.board

        menu_btn = Button(img_name=self.folder_path / "menu.png")
        left_arrow_btn = Button(img_name=self.folder_path / "left_arrow.png", action=board.undo_move)
        right_arrow_btn = Button(img_name=self.folder_path / "right_arrow.png", action=board.redo_move)
        restart_btn = Button(img_name=self.folder_path / "restart.png", action=self.game.new_game)
        puzzle_btn = Button(img_name=self.folder_path / "puzzle.png", action=self.game.set_challenge_mode)

        # left
        self.add_item(menu_btn)

        # right
        self.add_item(restart_btn, True)
        self.add_item(puzzle_btn, True)
        self.add_item(right_arrow_btn, True)
        self.add_item(left_arrow_btn, True)

    def set_images(self):
        self.button_images = {
            path: self.game.get_texture(path, self.button_size, True)
            for path in
            (list(self.button_images.keys()) if self.button_images else (ASSETS_PATH / "nav_bar_emojis").glob("*.png"))
        }


