from base_objects.button import Button
from base_objects.rect_object import RectObject
from globals import *
from container import VerticalContainer, HorizontalContainer


class NavigationBar(HorizontalContainer):
    def __init__(self, game, pos=(0, 0), size=RESOLUTION):
        super(NavigationBar, self).__init__(pos, size)

        self.game = game
        self.folder_path = ASSETS_PATH / "nav_bar_emojis"
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

        restart_btn = Button(img_name=self.folder_path / "restart.png", action=self.game.restart)
        switch_btn = Button(img_name=self.switch_img_name, action=self.game.change_mode)
        stack = VerticalContainer(size=(restart_btn.width, restart_btn.height + switch_btn.height))

        # left
        self.add_item(menu_btn)

        # right
        self.add_item(stack, True)
        self.add_item(right_arrow_btn, True)
        self.add_item(left_arrow_btn, True)

        stack.add_item(restart_btn)
        stack.add_item(switch_btn)

    def set_images(self):
        self.button_images = {
            path: self.game.get_texture(path, self.button_size, True)
            for path in (list(self.button_images.keys()) if self.button_images else (ASSETS_PATH / "nav_bar_emojis").glob("*.png"))
        }
