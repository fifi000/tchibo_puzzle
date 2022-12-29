import math


class CircleObject:
    radius = 10
    game = None

    def __init__(self, pos=(0, 0)):
        self.pos = self.x, self.y = pos

    @classmethod
    def set_globals(cls, radius, game):
        cls.radius = radius
        cls.game = game

    def check_collision(self, pos, radius_scale=1.0) -> bool:
        return math.dist(self.pos, pos) <= CircleObject.radius * radius_scale
