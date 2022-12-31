from base_objects.rect_object import RectObject


class NavBar(RectObject):
    def __init__(self, game, pos=(0, 0), size=(0, 0)):
        super(NavBar, self).__init__(pos, size)

        self.game = game

        self.left_items = []
        self.right_items = []

    @property
    def items(self):
        return self.left_items + self.right_items

    # MENU          < > RESTART
    def draw(self):
        for item in self.items:
            self.game.screen.blit(item.img, (item.x, item.y))

    def add_item(self, item, reverse_order=False):
        gap = 50

        item.y = self.y + (self.height - item.img.get_height())/2
        if not reverse_order:
            item.x = self.left_items[-1].img.get_width() + gap if self.left_items else self.x
            self.left_items.append(item)
        else:
            item.x = self.right_items[-1].x - gap - item.img.get_width() if self.right_items else self.x + self.width - item.img.get_width()
            self.right_items.append(item)

    # loop through items and fire their event
    def check_collision(self, pos):
        if item := next((item for item in self.items if item.check_collision(pos)), None):
            item.action()


