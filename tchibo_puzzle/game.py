import datetime
import pickle
import pygame as pg
from tkinter import messagebox, filedialog

from settings import *
from board import Board


class Game:
    def __init__(self):
        pg.init()

        self.board = None
        self.lifted_ball = None

        self.screen = pg.display.set_mode(RESOLUTION)

        self.background = Game.get_texture(ASSETS_PATH / "background.png", RESOLUTION)
        self.move_sound = pg.mixer.Sound(ASSETS_PATH / "move_sound.mp3")

        self.new_game()

    @staticmethod
    def get_texture(path, size):
        return pg.transform.scale(pg.image.load(path).convert_alpha(), size)

    # old version
    def save_board(self):
        # save only if half of the board is empty
        if len(self.board.balls) > len(self.board.empty_fields):
            return

        # check if folder with current date exists
        if not (path := (GAMES_PATH / f"{datetime.date.today()}")).exists():
            path.mkdir()

        filled = FILLED_FIELD
        empty = EMPTY_FIELD
        time = "_".join(str(datetime.datetime.today()).replace(".", " ").split()[1].split(":")[:-1])
        with (path / f"{time}({len(self.board.balls)}).txt").open("w") as file:
            for grid in self.board.move_tracker.moves:
                rows = [
                    "".join(f"{(filled if cell.ball else empty) if cell else empty:3}" for cell in row) + "\n"
                    for row in grid
                ]
                file.writelines(rows)
                file.write("\n")

    def save_board_positions(self):
        # save only if at least half of the board is empty
        if len(self.board.balls) > len(self.board.empty_fields):
            return

        # check if folder with saved games exists
        if not (path := GAMES_PATH).exists():
            path.mkdir()

        # check if folder with current date exists
        if not (path := (GAMES_PATH / f"{datetime.date.today()}")).exists():
            path.mkdir()

        # file name -> [time when game ended]([balls left]).txt
        # eg. 22_45(3).txt
        time = "_".join(str(datetime.datetime.today()).replace(".", " ").split()[1].split(":")[:-1])
        file_name = f"{time}({len(self.board.balls)}).txt"

        with (path / file_name).open("wb") as file:
            pickle.dump(self.board.move_tracker.positions, file)

    def new_game(self):
        self.lifted_ball = None
        if self.board:
            self.save_board_positions()

        gap = 50
        size = WIDTH - 2 * gap, HEIGHT - 2 * gap
        self.board = Board(self, size, (gap, gap))

    def draw(self):
        # self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, 0))
        self.board.draw()
        pg.display.flip()

    def lift_ball(self):
        if ball := next((b for b in self.board.balls if b.check_collision(pg.mouse.get_pos())), None):
            ball.clicked = True
            self.lifted_ball = ball

    def drop_ball(self):
        try:
            old_field = [f for f in self.board.fields if f.ball == self.lifted_ball][0]
        except IndexError:
            self.lifted_ball = None
            return

        if field := next((f for f in self.board.fields if f.check_collision(pg.mouse.get_pos(), 1.5)), None):
            if self.board.move_ball(old_field, field):
                self.move_sound.play()
        self.lifted_ball.clicked = False
        self.lifted_ball = None

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.save_board_positions()
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN and not self.lifted_ball:
                self.lift_ball()
            if event.type == pg.MOUSEBUTTONUP and self.lifted_ball:
                self.drop_ball()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    if messagebox.askyesno("Restart Game", "Do you really want to restart?"):
                        self.new_game()
                if event.key in [pg.K_LEFT, pg.K_a]:
                    self.board.undo_move()
                if event.key in [pg.K_RIGHT, pg.K_d]:
                    self.board.redo_move()
                if event.key == pg.K_m:
                    print("menu")
                if event.key == pg.K_l:
                    path = filedialog.askopenfilename(
                        title="File to load",
                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                        initialdir=GAMES_PATH
                    )
                    if path:
                        try:
                            file = open(path, "rb")
                            self.new_game()
                            self.board.load_board(pickle.load(file))
                        except IOError:
                            messagebox.showerror("File Error", "Could not open this file.")

    def get_grids_from_file(self, path):
        try:
            with open(path) as file:
                grids = [
                    ["".join(row).split() for row in grid.split("\n")]
                    for grid in file.read().split("\n\n")
                ]
                print(grids[0][0])
                self.board.load_board(grids)
        except FileNotFoundError:
            pass

    def run(self):
        while True:
            self.check_events()
            self.draw()
