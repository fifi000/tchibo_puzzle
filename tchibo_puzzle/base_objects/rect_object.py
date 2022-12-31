

class RectObject:
    def __init__(self, pos, size):
        self.set_pos(pos)
        self.set_size(size)

    def set_pos(self, pos):
        self.pos = self.x, self.y = pos

    def set_size(self, size):
        self.size = self.width, self.height = size

    def check_collision(self, pos) -> bool:
        x, y = pos
        return (
            self.x <= x <= self.x + self.width and
            self.y <= y <= self.y + self.height
        )
