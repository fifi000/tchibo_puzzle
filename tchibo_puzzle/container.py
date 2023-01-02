from base_objects.rect_object import RectObject


class Container(RectObject):
    def __init__(self, pos=(0, 0), size=(0, 0), gap=20):
        super(Container, self).__init__(pos, size)

        self.gap = gap

        self.group1 = []
        self.group2 = []

    @property
    def items(self):
        return self.group1 + self.group2

    def draw(self):
        for item in self.items:
            item.draw()

    def add_item(self, item, reverse_order=False):
        pass

    def add_items(self, items, reverse_order=False):
        for item in items:
            self.add_item(item, reverse_order)

    # loop through items and fire their event
    def check_collision(self, pos):
        if item := next((item for item in self.items if item.check_collision(pos)), None):
            item.action()


class HorizontalContainer(Container):
    def __init__(self, pos=(0, 0), size=(0, 0)):
        super(HorizontalContainer, self).__init__(pos, size)

    def add_item(self, item, reverse_order=False):
        item.y = self.y + (self.height - item.height)/2
        if not reverse_order:
            item.x = self.group1[-1].width + self.gap if self.group1 else self.x
            self.group1.append(item)
        else:
            item.x = self.group2[-1].x - self.gap - item.width if self.group2 else self.x + self.width - item.width
            self.group2.append(item)


class VerticalContainer(Container):
    def __init__(self, pos=(0, 0), size=(0, 0)):
        super(VerticalContainer, self).__init__(pos, size)

    def add_item(self, item, reverse_order=False):
        item.x = self.x + (self.width - item.width)/2
        if not reverse_order:
            item.y = self.group1[-1].height + self.gap if self.group1 else self.y
            self.group1.append(item)
        else:
            item.y = self.group2[-1].y - self.gap - item.height if self.group2 else self.y + self.height - item.height
            self.group2.append(item)

