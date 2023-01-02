from base_objects.button import Button
from base_objects.rect_object import RectObject
from globals import *
from container import VerticalContainer, HorizontalContainer


class NavigationBar(HorizontalContainer):
    def __init__(self, game, pos=(0, 0), size=RESOLUTION):
        super(NavigationBar, self).__init__(pos, size)

        self.game = game
        self.button_images = None
        self.set_images()

    @property
    def button_size(self):
        return self.height, self.height

    def resize(self):
        print()

    def init_buttons(self):
        path = ASSETS_PATH / "nav_bar_emojis"
        board = self.game.board

        self.right_arrow_btn = Button(img_name=path / "right_arrow.png", action=board.redo_move)
        self.left_arrow_btn = Button(img_name=path / "left_arrow.png", action=board.undo_move)
        self.restart_btn = Button(img_name=path / "restart.png", action=self.game.new_game)
        self.switch_off_btn = Button(img_name=path / "switch_off.png", action=self.game.challenge_mode)
        self.menu_btn = Button(img_name=path / "menu.png")

        # left
        self.add_item(self.menu_btn)

        # right
        self.add_item(self.restart_btn, True)
        self.add_item(self.right_arrow_btn, True)
        self.add_item(self.left_arrow_btn, True)

    def set_images(self):
        self.button_images = {
            path: self.game.get_texture(path, self.button_size, True)
            for path in (list(self.button_images.keys()) if self.button_images else (ASSETS_PATH / "nav_bar_emojis").glob("*.png"))
        }
