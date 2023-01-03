if __name__ == '__main__':
    from game import Game
    import pygame as pg

    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        game.save_board_positions()
        pg.quit()
