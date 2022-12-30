import pygame as pg
from random import choice

from settings import *
from ball import Ball
from circle_object import CircleObject

_ = None
field_grid = [
    [_, _, 1, 1, 1, _, _],
    [_, _, 1, 1, 1, _, _],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [_, _, 1, 1, 1, _, _],
    [_, _, 1, 1, 1, _, _],
]


def show_grid(g):
    print("=" * 50)
    for row in [[cell if cell else "_" for cell in row] for row in g]:
        for cell in row:
            print(f"{str(cell):3}", end="")
        print()
    print()


class MoveTracker:
    def __init__(self, init_grid):
        self.moves = [MoveTracker.copy_grid(init_grid)]
        self.index_tracker = 0

        # [(old_field, new_field), ...]
        self.positions = []

    def add_move(self, grid):
        grid = MoveTracker.copy_grid(grid)
        while self.index_tracker != len(self.moves) - 1:
            self.moves.pop()
            self.positions.pop()
        self.moves.append(grid)
        self.index_tracker += 1

    def undo_move(self):
        if self.index_tracker > 0:
            self.index_tracker -= 1
            return MoveTracker.copy_grid(self.moves[self.index_tracker])

    def redo_move(self):
        if self.index_tracker != len(self.moves) - 1:
            self.index_tracker += 1
            return MoveTracker.copy_grid(self.moves[self.index_tracker])

    @staticmethod
    def copy_grid(grid):
        return [[cell.__copy__() if cell else cell for cell in row] for row in grid]


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
        surface = pg.Surface((self.radius*2, self.radius*2))
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


class Board:
    def __init__(self, game, size=RESOLUTION, pos=(0, 0)):
        self.game = game

        self.size = self.width, self.height = size
        self.pos = self.x, self.y = pos

        self.grid = field_grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.radius = self.height / (self.rows*3 - 1)
        self.diameter = 2 * self.radius

        self.ball_images = [
            self.game.get_texture(path, (self.diameter, self.diameter))
            for path in (ASSETS_PATH / "Balls").glob("*.png")
        ]

        CircleObject.set_globals(self.radius, self.game)
        self.grid = self.__get_fields()
        self.__set_balls()

        self.move_tracker = MoveTracker(self.grid)

    @property
    def fields(self):
        return [field for row in self.grid for field in row if field]

    @property
    def balls(self):
        return [f.ball for f in self.fields if f.ball]

    @property
    def empty_fields(self):
        return [f for f in self.fields if not f.ball]

    def __set_balls(self):
        for i, field in enumerate(self.fields):
            if i == len(self.fields) // 2:  # skip center field
                continue
            field.ball = Ball(field.pos, img=choice(self.ball_images))

    def __get_fields(self) -> list[list[Field]]:
        start_x, start_y = self.x + self.radius, self.y + self.radius
        dist = self.radius * 3

        return [
            [
                Field((start_x + dist*j, start_y + dist*i), i, j) if cell else None
                for j, cell in enumerate(row)
            ]
            for i, row in enumerate(self.grid)
        ]

    def load_board(self, positions):
        for old, new in positions:
            old_field = self.grid[old[0]][old[1]]
            new_field = self.grid[new[0]][new[1]]
            self.move_ball(old_field, new_field)

        # begin with filled board
        self.move_tracker.index_tracker = 1
        self.undo_move()

    def move_ball(self, old_field, new_field) -> bool:
        def handle_middle_ball(row, col):
            if (middle := self.grid[row][col]).ball:
                middle.ball = None
                new_field.add_ball(old_field.ball)
                old_field.ball = None
                return True
            return False

        # prevent placing one ball onto another
        if old_field.ball:
            return False

        output = False
        # same row and 2 columns apart
        if new_field.row == old_field.row and abs(new_field.col - old_field.col) == 2:
            output = handle_middle_ball(new_field.row, (old_field.col + new_field.col)//2)

        # same column and 2 rows apart
        if new_field.col == old_field.col and abs(new_field.row - old_field.row) == 2:
            output = handle_middle_ball((old_field.row + new_field.row)//2, new_field.col)

        if output:
            self.move_tracker.add_move(self.grid)
            self.move_tracker.positions.append(((old_field.row, old_field.col), (new_field.row, new_field.col)))

        return output

    def redo_move(self):
        if grid := self.move_tracker.redo_move():
            self.grid = grid
            self.game.move_sound.play()

    def undo_move(self):
        if grid := self.move_tracker.undo_move():
            self.grid = grid
            self.game.move_sound.play()

    def draw(self):
        for field in self.fields:
            field.draw()

        # draw lifted ball
        [b.draw() for b in self.balls if b.clicked]
