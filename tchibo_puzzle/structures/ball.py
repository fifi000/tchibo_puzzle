import pygame as pg

from base_objects.circle_object import CircleObject
from globals import BLACK


class Ball(CircleObject):
    def __init__(self, pos=(0, 0), color=BLACK, img=None):
        super(Ball, self).__init__(pos)
        self.clicked = False
        self.color = color
        self.img = img

    def draw(self):
        x, y = self.pos if not self.clicked else pg.mouse.get_pos()
        if self.img.img:
            x -= self.radius
            y -= self.radius
            self.game.screen.blit(self.img.img, (x, y))
        else:
            pg.draw.circle(self.game.screen, self.color, (x, y), self.radius)

    def __copy__(self):
        return self.__class__(self.pos, self.color, self.img.img)

