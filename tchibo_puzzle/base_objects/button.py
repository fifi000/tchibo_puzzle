from base_objects.rect_object import RectObject


class Button(RectObject):
    game = None

    def __init__(self, pos=(0, 0), img_name=None, action=None):
        self.img_name = img_name

        super(Button, self).__init__(pos, self.img.get_size())

        if action:
            self.action = action

    @property
    def img(self):
        # return self.game.board.ball_images[self.img_name]
        return self.img_name

    def draw(self):
        self.game.screen.blit(self.img, self.pos)

    def action(self):
        pass

