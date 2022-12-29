import math

import pygame as pg

from circle_object import CircleObject
from settings import BLACK


class Ball(CircleObject):
    def __init__(self, pos, color=BLACK, img=None):
        super(Ball, self).__init__(pos)
        self.clicked = False
        self.color = color
        self.img = img

    def draw(self):
        x, y = self.pos if not self.clicked else pg.mouse.get_pos()
        if self.img:
            x -= self.radius
            y -= self.radius
            self.game.screen.blit(self.img, (x, y))
        else:
            pg.draw.circle(self.game.screen, self.color, (x, y), self.radius)

    def __copy__(self):
        return self.__class__(self.pos, self.color, self.img)

