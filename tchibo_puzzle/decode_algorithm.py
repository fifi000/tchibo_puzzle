from settings import *

filled = FILLED_FIELD
empty = EMPTY_FIELD
patterns = [
    (filled, filled, empty),
    (empty, filled, filled),
]
empty_pattern = tuple(empty for _ in range(3))


def foo(grids):
    # [(old_field_pos, new_field_pos), ...]
    output = []

    # check rows
    for grid1, grid2 in zip(grids, grids[1:]):
        check_2_grids(grid1, grid2)


def check_2_grids(grid1, grid2):
    for i, (row1, row2) in enumerate(zip(grid1, grid2)):
        for j, (a, b, c) in enumerate(zip(row1[:-2], row1[1:-1], row1[2:])):
            if (a, b, c) in patterns and (row2[j], row2[j + 1], row2[j + 2]).count(empty) == 2:
                # O O _  ==>  _ _ O
                if (a, b, c) == (filled, filled, empty):
                    return (i, j), (i, j+3)
                # _ O O  ==>  O _ _
                else:
                    return (i, j+3), (i, j)
