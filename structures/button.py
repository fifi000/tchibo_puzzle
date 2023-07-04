from structures.base_objects.rect_object import RectObject


class Button(RectObject):
    game = None

    def __init__(self, pos=(0, 0), img_name=None, action=None):
        self.img_name = img_name

        super(Button, self).__init__(pos, self.img.get_size())

        if action:
            self.action = action

    @property
    def img(self):
        return self.game.nav_bar.button_images.get(self.img_name, None)

    def draw(self):
        if img := self.img:
            self.game.screen.blit(img, self.pos)

    def action(self):
        pass
