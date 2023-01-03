import pygame as pg

from globals import *
from structures.base_objects.circle_object import CircleObject


class Field(CircleObject):
    def __init__(self, pos=(0, 0), row=0, col=0, ball=None):
        super(Field, self).__init__(pos)
        self.row = row
        self.col = col
        self.ball = ball

    def draw(self):
        # pg.draw.circle(Field.game.screen, WHITE, self.pos, self.radius)

        # draw transparent circle
        circle_color = WHITE if not self.ball else GRAY
        surface = pg.Surface((self.radius * 2, self.radius * 2))
        surface.set_colorkey((0, 0, 0))
        surface.set_alpha(100)
        pg.draw.circle(surface, circle_color, (self.radius, self.radius), self.radius)
        self.game.screen.blit(surface, (self.x - self.radius, self.y - self.radius))

        if self.ball:
            self.ball.draw()

    def add_ball(self, ball):
        ball.pos = self.pos
        self.ball = ball

    def __repr__(self):
        return "1" if self.ball else "_"

    def __copy__(self):
        ball = self.ball.__copy__() if self.ball else None
        return Field(self.pos, self.row, self.col, ball)
