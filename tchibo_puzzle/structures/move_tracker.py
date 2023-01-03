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
