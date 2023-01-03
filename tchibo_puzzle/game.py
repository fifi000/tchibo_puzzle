import datetime
import pickle
from random import random
from tkinter import messagebox, filedialog

import pygame as pg
from easygui import enterbox

from board import Board
from container import VerticalContainer
from globals import *
from navigation_bar import NavigationBar
from structures.button import Button
from structures.move_tracker import MoveTracker


def help_info():
    li = [
        "H - help info",
        "A / left-arrow - undo",
        "D / right-arrow - redo",
        "C - challenge mode",
        "R - new game",
        "L - load game to analise",
    ]
    text = "\n".join([s for s in li])
    messagebox.askokcancel(
        title="Help",
        message=text
    )


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(
            size=RESOLUTION,
            flags=pg.RESIZABLE
        )
        pg.display.set_caption(CAPTION)
        Button.game = self

        self.nav_bar = None
        self.board = None
        self.lifted_ball = None
        self.reversed = None
        self.loaded = None
        self.container = None

        self.challenge_mode = False

        self.background = Game.get_texture(ASSETS_PATH / "background.png", self.screen.get_size())

        sounds = (ASSETS_PATH / "sounds")
        self.move_sound = pg.mixer.Sound(sounds / "move_sound.mp3")
        self.switch_sound = pg.mixer.Sound(sounds / "switch_sound.wav")
        self.switch_sound.set_volume(0.1)

        self.new_game(save=False)

    @property
    def gap(self):
        return GAP * min(self.screen.get_size())

    @property
    def board_size(self):
        return self.game_width, self.game_height * 0.92

    @property
    def nav_bar_size(self):
        return self.game_width, self.game_height - self.board_size[1]

    @property
    def game_width(self):
        return self.screen.get_width() - 2 * self.gap

    @property
    def game_height(self):
        return self.screen.get_height() - 2 * self.gap

    @staticmethod
    def get_texture(path, size, rect_proportions=False):
        img = pg.image.load(path).convert_alpha()
        return Game.resize_texture(img, size, rect_proportions)

    @staticmethod
    def resize_texture(img, size, rect_proportions=False):
        if rect_proportions:
            k = max(img.get_size()) / max(size)
            size = tuple(s / k for s in img.get_size())
        return pg.transform.scale(img, size)

    def new_game(self, save=True):
        self.lifted_ball = None
        if self.board and save:
            self.save_board_positions()

        self.reversed = False
        self.loaded = False

        self.board = Board(
            self,
            size=self.board_size
        )

        self.handle_screen_resize()

    def set_container(self):
        self.container = VerticalContainer(
            pos=(self.gap, self.gap),
            size=(self.game_width, self.game_height),
        )
        self.container.gap = self.gap

        self.nav_bar = NavigationBar(
            self,
            size=(self.game_width, int(self.game_height * 0.08))
        )

        self.board.resize(self.board_size)

        self.container.add_items((self.nav_bar, self.board))

    def get_level(self):
        n = enterbox(
            title="Level",
            msg="Enter balls number [2-32]",
            default="10"
        )
        try:
            return max(int(n), 2) % len(self.board.fields) - 1
        except:
            return None

    def set_challenge_mode(self, level=10):
        def is_valid_move(move):
            row, col = field.row + move[0], field.col + move[1]
            # grid boundary
            if 0 <= row <= len(self.board.grid) - 1 and 0 <= col <= len(self.board.grid[0]) - 1:
                # validate field
                if (new_field := self.board.grid[row][col]) and not new_field.ball and self.board.move_ball(field,
                                                                                                            new_field,
                                                                                                            reversed_move=True):
                    return True
            return False

        def try_move():
            # moves -> [left, right, up, down]
            for move in sorted([(0, -2), (0, 2), (2, 0), (-2, 0)], key=lambda x: random()):
                if is_valid_move(move):
                    return True
            return False

        self.new_game(save=False)

        # clear board
        for field in self.board.fields:
            field.ball = None
        self.board.set_ball_center()

        # choose random ball
        # if has valid move -> move there
        for _ in range(level):
            for field in sorted([f for f in self.board.fields if f.ball], key=lambda x: random()):
                if try_move():
                    break

        # remove generated moves form Move Tracker
        self.board.move_tracker = MoveTracker(self.board.grid)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.container.draw()
        pg.display.flip()

    def handle_screen_resize(self):
        self.set_container()

        self.board.resize(self.board_size)
        self.nav_bar.init_buttons()

        self.background = Game.get_texture(ASSETS_PATH / "background.png", self.screen.get_size())

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

    def save_board_positions(self):
        # save only if at least half of the board is empty
        # game is not reversed
        # not challenge mode
        if (len(self.board.balls) / len(self.board.fields) > MIN_BALLS_TO_SAVE
                or self.reversed
                or self.challenge_mode):
            return

        # check if folder with saved games exists
        if not (path := GAMES_PATH).exists():
            path.mkdir()

        # check if folder with current date exists
        if not (path := (GAMES_PATH / f"{datetime.date.today()}")).exists():
            path.mkdir()

        # _file name -> [time when game ended]([balls left]).txt
        # eg. 22_45(3).txt
        time = "_".join(str(datetime.datetime.today()).replace(".", " ").split()[1].split(":")[:-1])
        file_name = f"{time}({len(self.board.balls)}).txt"

        with (path / file_name).open("wb") as file:
            pickle.dump(self.board.move_tracker.positions, file)

    def load_game(self):
        if path := filedialog.askopenfilename(
                title="File to load",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialdir=GAMES_PATH
        ):
            try:
                with open(path, "rb") as file:
                    self.new_game()
                    self.loaded = True
                    self.board.load_board(pickle.load(file))
            except IOError:
                messagebox.showerror("File Error", "Could not open this file.")

    def restart(self):
        if self.challenge_mode:
            if level := self.get_level():
                self.set_challenge_mode(level)
        else:
            self.new_game()

    def change_mode(self):
        self.switch_sound.play()
        self.challenge_mode ^= True
        self.handle_screen_resize()

    def check_events(self):
        for event in (events := pg.event.get()):
            if event.type == pg.QUIT:
                self.save_board_positions()
                pg.quit()
                exit()
            if event.type == pg.WINDOWSIZECHANGED:
                self.handle_screen_resize()
            if event.type == pg.MOUSEBUTTONDOWN and not self.lifted_ball:
                self.lift_ball()
            if event.type == pg.MOUSEBUTTONUP and self.lifted_ball:
                self.drop_ball()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.restart()
                if event.key in [pg.K_LEFT, pg.K_a]:
                    self.board.undo_move()
                if event.key in [pg.K_RIGHT, pg.K_d]:
                    self.board.redo_move()
                if event.key == pg.K_l:
                    self.load_game()
                if event.key == pg.K_c:
                    self.change_mode()
                if event.key == pg.K_h:
                    help_info()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.nav_bar.check_collision(pg.mouse.get_pos())

    def run(self):
        while True:
            self.check_events()
            self.draw()
