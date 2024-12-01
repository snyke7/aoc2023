from attrs import define


# for: https://hack.ainfosec.com/


test_input = '''|  3 |  11 |   X |   5 |  10 |
|  7 |   6 |   2 |  15 |   4 |
| 13 |   8 |   1 |  22 |  19 |
| 17 |  18 |  23 |  20 |   9 |
| 14 |  12 |  16 |  21 |  24 | '''

test_input2 = '''|  7 |   X |  17 |   9 |   5 |
| 23 |   8 |  16 |  12 |  18 |
|  1 |  21 |  24 |   4 |  10 |
|  6 |  11 |  19 |  14 |  15 |
| 22 |   3 |  20 |  13 |   2 | '''

test_input3 = '''|  8 |   4 |   7 |   5 |  10 |
| 20 |   1 |   2 |   9 |  22 |
|  3 |  16 |   6 |  14 |  23 |
| 19 |  12 |  15 |  21 |  13 |
| 11 |  17 |  18 |   X |  24 | '''

test_input4 = '''| 14 |   8 |  10 |   1 |   5 |
|  9 |   7 |   6 |   4 |  20 |
| 11 |   X |   2 |  15 |   3 |
| 18 |  13 |  19 |  23 |  12 |
| 21 |  22 |  17 |  16 |  24 | '''

test_input5 = '''|  1 |   2 |   4 |   7 |   5 |
|  6 |   8 |   3 |   9 |  10 |
| 16 |  12 |   X |  14 |  19 |
| 17 |  11 |  20 |  18 |  15 |
| 23 |  13 |  21 |  22 |  24 | '''

test_input6 = '''| 19 |   5 |   1 |   3 |   4 |
|  7 |   2 |  13 |  18 |  14 |
|  6 |  11 |   X |  12 |   8 |
| 17 |  21 |  10 |  23 |   9 |
| 16 |  22 |  24 |  15 |  20 | '''

test_input7 = '''|  6 |  13 |   3 |   5 |  10 |
|  7 |   1 |   9 |  17 |   4 |
|  X |   8 |  22 |  14 |  15 |
| 16 |  18 |  11 |   2 |  20 |
| 12 |  21 |  23 |  19 |  24 | '''

test_input8 = '''|  1 |   2 |   4 |  14 |   X |
|  7 |  11 |   3 |   5 |   8 |
|  6 |  12 |  13 |   9 |  23 |
| 21 |  16 |  18 |  15 |  10 |
| 19 |  17 |  22 |  24 |  20 | '''


def read_input(input_str):
    output = [
        [
            int(el.replace('X', '0').strip()) - 1
            for el in line[:-1].split('|')[1:]
            if el.strip()
        ] for line in input_str.splitlines()
    ]
    return output


def get_coord_of(state, tile):
    return next(((i, j) for i in range(5) for j in range(5) if state[i][j] == tile))


def move_hole_right(state):
    hole_row, hole_col = get_coord_of(state, -1)
    return [
        row if i != hole_row else row[:hole_col] + [row[hole_col + 1], row[hole_col]] + row[hole_col+2:]
        for i, row in enumerate(state)
    ]


def move_hole_left(state):
    hole_row, hole_col = get_coord_of(state, -1)
    return [
        row if i != hole_row else row[:hole_col-1] + [row[hole_col], row[hole_col-1]] + row[hole_col+1:]
        for i, row in enumerate(state)
    ]


def transpone(state):
    return [[state[j][i] for j in range(5)] for i in range(5)]


def move_hole_up(state):
    return transpone(move_hole_left(transpone(state)))


def move_hole_down(state):
    return transpone(move_hole_right(transpone(state)))


@define
class State:
    cur_state: [[int]]
    path: [str] = []

    def move_left(self):
        self.cur_state = move_hole_left(self.cur_state)
        self.path += ['L']

    def move_right(self):
        self.cur_state = move_hole_right(self.cur_state)
        self.path += ['R']

    def move_down(self):
        self.cur_state = move_hole_down(self.cur_state)
        self.path += ['D']

    def move_up(self):
        self.cur_state = move_hole_up(self.cur_state)
        self.path += ['U']

    def move(self, els):
        for el in els:
            if el == 'L':
                self.move_left()
            elif el == 'R':
                self.move_right()
            elif el == 'U':
                self.move_up()
            elif el == 'D':
                self.move_down()
            else:
                raise ValueError(el)

    def get_coord(self, tile):
        return get_coord_of(self.cur_state, tile)

    def get_pretty_path(self):
        return ','.join(self.path)


def move_hole_to(state: State, dest_x, dest_y):
    while True:
        hole_x, hole_y = state.get_coord(-1)
        if hole_y < dest_y:
            state.move_right()
        elif hole_y == dest_y:
            if hole_x < dest_x:
                state.move_down()
            elif hole_x == dest_x:
                break
            else:
                state.move_up()
        else:
            state.move_left()


def move_hole_to_prio_ud(state: State, dest_x, dest_y):
    while True:
        hole_x, hole_y = state.get_coord(-1)
        if hole_x < dest_x:
            state.move_down()
        elif hole_x == dest_x:
            if hole_y < dest_y:
                state.move_right()
            elif hole_y == dest_y:
                break
            else:
                state.move_left()
        else:
            state.move_up()


def move_tile_right(state, tile):
    assert tile != -1
    cur_x, cur_y = state.get_coord(tile)
    hole_x, hole_y = state.get_coord(-1)
    if hole_x == cur_x:  # if hole_x == cur_x, hole movements could move the tile
        if hole_y > cur_y:  # we are in a great spot: just move left a couple of times
            for i in range(hole_y - cur_y):
                state.move_left()
                return
        else:
            if hole_x < 4:
                state.move_down()
            else:
                state.move_up()
    elif hole_x < cur_x and hole_y > cur_y + 1:
        # moving left is possibly bad
        state.move_down()
    move_hole_to(state, cur_x, cur_y + 1)
    # above will not move tile, since hole will first fix its left/right position

    # at this point, the hole is to the left of the tile, so we just move left
    state.move_left()


def move_tile_left(state, tile):
    assert tile != -1
    cur_x, cur_y = state.get_coord(tile)
    hole_x, hole_y = state.get_coord(-1)
    if hole_x == cur_x:  # if hole_x == cur_x, hole movements could move the tile
        if hole_y < cur_y:  # we are in a great spot: just move right a couple of times
            for i in range(cur_y - hole_y):
                state.move_right()
                return
        else:
            if hole_x < 4:
                state.move_down()
            else:
                state.move_up()
    move_hole_to(state, cur_x, cur_y - 1)
    # above will not move tile, since hole will first fix its left/right position

    # at this point, the hole is to the left of the tile, so we just move left
    state.move_right()


def move_tile_up(state, tile):
    assert tile != -1
    cur_x, cur_y = state.get_coord(tile)
    hole_x, hole_y = state.get_coord(-1)
    if hole_y == cur_y:  # if hole_x == cur_x, hole movements could move the tile
        if hole_x < cur_x:  # we are in a great spot: just move down a couple of times
            for i in range(cur_x - hole_x):
                state.move_down()
                return
        else:
            if hole_y < 4:
                state.move_right()
            else:  # this assumes someone else takes precautions to ensure this is safe
                state.move_left()
    elif hole_y < cur_y and hole_x >= cur_x and (cur_y < 4 and cur_x < 4):
        # we could disturb previously correct things if we directly move to above
        # instead, we go around, since this is possible in this case
        move_hole_to_prio_ud(state, cur_x + 1, cur_y + 1)
    move_hole_to_prio_ud(state, cur_x - 1, cur_y)
    # above will not move tile, since hole will first fix its up/down position

    # at this point, the hole is above of the tile, so we just move down
    state.move_down()


def fix_tile(state: State, tile):
    dest_x, dest_y = tile // 5, tile % 5
    # we assume everything above dest_x and left of dest_y is correct, and should not disturb it
    while True:
        cur_x, cur_y = state.get_coord(tile)
        if cur_y < dest_y:  # if this is the case, we must have cur_x > dest_x
            move_tile_right(state, tile)
        elif cur_y > dest_y:
            move_tile_left(state, tile)
        elif cur_x > dest_x:
            if cur_x == dest_x + 1 and dest_y == 4:
                # we will disturb the row if not careful
                move_hole_to(state, cur_x, 2)
                state.move_up()
                state.move_right()
                state.move_right()
                state.move_down()
                state.move_left()
                state.move_up()
                state.move_left()
                state.move_down()
            else:
                move_tile_up(state, tile)
        else:
            break


def fix_row(state: State, row):
    for i in range(5):
        fix_tile(state, row * 5 + i)


def fix_n_print_tile(state, tile, do_print=True):
    fix_tile(state, tile)
    if do_print:
        print(state.cur_state)
        print(state.get_pretty_path())


def fix_n_print_row(state, row, do_print=True):
    fix_row(state, row)
    if do_print:
        print(state.cur_state)
        print(state.get_pretty_path())


def main():
    result = read_input('''|  6 |   7 |   8 |   4 |   5 |
|  2 |  22 |   1 |   3 |  10 |
| 11 |  16 |   9 |  13 |  15 |
| 21 |  14 |  20 |  24 |   X |
| 23 |  12 |  19 |  18 |  17 | ''')
    state = State(result)
    print(state.cur_state)
    print(state.get_pretty_path())
    fix_n_print_row(state, 0)
    fix_n_print_row(state, 1)
    fix_n_print_row(state, 2)
    print(state.cur_state)
    print(state.get_pretty_path())


if __name__ == '__main__':
    main()
