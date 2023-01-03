from random import choice

from globals import *
from structures.ball import Ball
from structures.base_objects.circle_object import CircleObject
from structures.base_objects.rect_object import RectObject
from structures.field import Field
from structures.move_tracker import MoveTracker

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


class Board(RectObject):
    def __init__(self, game, size=RESOLUTION, pos=(0, 0)):
        super(Board, self).__init__(pos, size)
        self.game = game

        self.grid = field_grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.ball_images = None
        self.set_images()

        CircleObject.game = self.game
        self.grid = self.__get_fields()

        if not self.game.reversed:
            self.set_balls()
        else:
            self.set_ball_center()

        self.move_tracker = None

    @property
    def balls_area_side_len(self):
        return min(self.size)

    @property
    def radius(self):
        return self.balls_area_side_len / (self.cols * 3 - 1)

    @property
    def diameter(self):
        return 2 * self.radius

    @property
    def fields(self):
        return [field for row in self.grid for field in row if field]

    @property
    def balls(self):
        return [f.ball for f in self.fields if f.ball]

    @property
    def empty_fields(self):
        return [f for f in self.fields if not f.ball]

    def set_images(self):
        # if not self.ball_images:
        self.ball_images = {
            path: self.game.get_texture(path, (self.diameter, self.diameter))
            for path in (list(self.ball_images.keys()) if self.ball_images else (ASSETS_PATH / "balls").glob("*.png"))
        }
        # else:
        #     self.ball_images = {
        #         path: self.game.resize_texture(img, (self.diameter, self.diameter))
        #         for path, img in self.ball_images.items()
        #     }

    def set_balls(self):
        for i, field in enumerate(self.fields):
            if i == len(self.fields) // 2:  # skip center field
                continue
            field.ball = Ball(field.pos, color=choice(list(self.ball_images.keys())))

    def set_ball_center(self):
        if field := next((field for i, field in enumerate(self.fields) if i == len(self.fields) // 2), None):
            field.ball = Ball(field.pos, color=choice(list(self.ball_images.keys())))

    def __get_fields(self) -> list[list[Field]]:
        start_x = self.x + self.radius + (self.width - self.balls_area_side_len) / 2
        start_y = self.y + self.radius + (self.height - self.balls_area_side_len) / 2
        dist = self.radius * 3

        return [
            [
                Field((start_x + dist * j, start_y + dist * i), i, j) if cell else None
                for j, cell in enumerate(row)
            ]
            for i, row in enumerate(self.grid)
        ]

    def resize(self, size):
        self.size = size
        self.set_images()

        start_x = self.x + self.radius + (self.width - self.balls_area_side_len) / 2
        start_y = self.y + self.radius + (self.height - self.balls_area_side_len) / 2
        dist = self.radius * 3

        for row in self.grid:
            for field in [f for f in row if f]:
                field.pos = (start_x + dist * field.col, start_y + dist * field.row)
                if ball := field.ball:
                    ball.pos = field.pos

    def load_board(self, positions):
        for old, new in positions:
            old_field = self.grid[old[0]][old[1]]
            new_field = self.grid[new[0]][new[1]]
            self.move_ball(old_field, new_field)

        # begin with filled board
        self.move_tracker.index_tracker = 1
        self.undo_move()

    def move_ball(self, old_field, new_field, reversed_move=False) -> bool:
        def handle_middle_ball(row, col):
            if (middle := self.grid[row][col]).ball:
                middle.ball = None
                new_field.add_ball(old_field.ball)
                old_field.ball = None
                return True
            return False

        def handle_middle_ball_reversed(row, col):
            if not (middle := self.grid[row][col]).ball:
                middle.add_ball(Ball(color=choice(list(self.ball_images.keys()))))
                new_field.add_ball(old_field.ball)
                old_field.ball = None
                return True
            return False

        if not self.move_tracker:
            self.move_tracker = MoveTracker(self.grid)

        if self.game.reversed or reversed_move:
            handle_middle_ball = handle_middle_ball_reversed

        # prevent placing one ball onto another
        if new_field.ball:
            return False

        output = False
        # same row and 2 columns apart
        if new_field.row == old_field.row and abs(new_field.col - old_field.col) == 2:
            output = handle_middle_ball(new_field.row, (old_field.col + new_field.col) // 2)

        # same column and 2 rows apart
        if new_field.col == old_field.col and abs(new_field.row - old_field.row) == 2:
            output = handle_middle_ball((old_field.row + new_field.row) // 2, new_field.col)

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
