import math


class CircleObject:
    game = None

    def __init__(self, pos=(0, 0)):
        self.pos = pos

    @property
    def radius(self):
        return self.game.board.radius

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def check_collision(self, pos, radius_scale=1.0) -> bool:
        return math.dist(self.pos, pos) <= self.radius * radius_scale
