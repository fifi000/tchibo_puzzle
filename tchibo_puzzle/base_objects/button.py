from base_objects.rect_object import RectObject


class Button(RectObject):
    def __init__(self, pos=(0, 0), size=(0, 0), img=None, action=None):
        super(Button, self).__init__(pos, size)

        self.img = img

        if self.img:
            self.set_size(self.img.get_size())
        if action:
            self.action = action

    def action(self):
        pass

