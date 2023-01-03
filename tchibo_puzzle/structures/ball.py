import pygame as pg

from globals import BLACK
from structures.base_objects.circle_object import CircleObject


class Ball(CircleObject):
    def __init__(self, pos=(0, 0), color="black"):
        super(Ball, self).__init__(pos)
        self.clicked = False
        self.color = color

    @property
    def img(self):
        return self.game.board.ball_images[self.color]

    def draw(self):
        x, y = self.pos if not self.clicked else pg.mouse.get_pos()
        if self.img:
            x -= self.radius
            y -= self.radius
            self.game.screen.blit(self.img, (x, y))
        else:
            pg.draw.circle(self.game.screen, BLACK, (x, y), self.radius)

    def __copy__(self):
        return self.__class__(self.pos, self.color)
