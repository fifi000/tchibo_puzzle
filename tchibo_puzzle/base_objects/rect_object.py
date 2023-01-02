

class RectObject:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def check_collision(self, pos) -> bool:
        x, y = pos
        return (
            self.x <= x <= self.x + self.width and
            self.y <= y <= self.y + self.height
        )
