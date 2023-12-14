TEST = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''


def parse_dish(input_lines):
    cubes = {
        (i, j)
        for i, line in enumerate(input_lines)
        for j, el in enumerate(line.strip())
        if el == '#'
    }
    rollers = {
        (i, j)
        for i, line in enumerate(input_lines)
        for j, el in enumerate(line.strip())
        if el == 'O'
    }
    return cubes, rollers, len(input_lines[0].strip())


def into_row_map(elements):
    cube_rows = {}
    for cube_x, cube_y in elements:
        if cube_y not in cube_rows:
            cube_rows[cube_y] = []
        cube_rows[cube_y].append(cube_x)
    return cube_rows


def roll_vert(cubes, rollers, size, *, is_north):
    result = set()
    cube_rows = into_row_map(cubes)
    roller_rows = into_row_map(rollers)
    for i in range(size):
        if i not in roller_rows:  # nothing to roll
            continue
        cube_row = cube_rows[i] if i in cube_rows else []
        boundaries = [-1] + sorted(cube_row) + [size]
        for cube_n, cube_s in zip(boundaries[:-1], boundaries[1:]):
            the_rollers = [roller_x for roller_x in roller_rows[i] if cube_n < roller_x < cube_s]
            the_range = range(cube_n + 1, cube_n + 1 + len(the_rollers)) if is_north else \
                range(cube_s - len(the_rollers), cube_s)
            for r in the_range:
                result.add((r, i))
    return result


def roll_north(cubes, rollers, size):
    return roll_vert(cubes, rollers, size, is_north=True)


def roll_south(cubes, rollers, size):
    return roll_vert(cubes, rollers, size, is_north=False)


def into_col_map(elements):
    cube_rows = {}
    for cube_x, cube_y in elements:
        if cube_x not in cube_rows:
            cube_rows[cube_x] = []
        cube_rows[cube_x].append(cube_y)
    return cube_rows


def roll_horiz(cubes, rollers, size, *, is_west):
    result = set()
    cube_cols = into_col_map(cubes)
    roller_cols = into_col_map(rollers)
    for i in range(size):
        if i not in roller_cols:  # nothing to roll
            continue
        cube_col = cube_cols[i] if i in cube_cols else []
        boundaries = [-1] + sorted(cube_col) + [size]
        for cube_w, cube_e in zip(boundaries[:-1], boundaries[1:]):
            the_rollers = [roller_y for roller_y in roller_cols[i] if cube_w < roller_y < cube_e]
            the_range = range(cube_w + 1, cube_w + 1 + len(the_rollers)) if is_west else \
                range(cube_e - len(the_rollers), cube_e)
            for r in the_range:
                result.add((i, r))
    return result


def roll_west(cubes, rollers, size):
    return roll_horiz(cubes, rollers, size, is_west=True)


def roll_east(cubes, rollers, size):
    return roll_horiz(cubes, rollers, size, is_west=False)


def single_cycle(cubes, rollers, size):
    the_rollers = rollers
    the_rollers = roll_north(cubes, the_rollers, size)
    the_rollers = roll_west(cubes, the_rollers, size)
    the_rollers = roll_south(cubes, the_rollers, size)
    the_rollers = roll_east(cubes, the_rollers, size)
    return the_rollers


def repeated_cycle(cubes, rollers, size, num_cycles):
    seen_hashes = {hash(frozenset(rollers)): 0}
    cur_cycle = 0
    cur_rollers = rollers
    while cur_cycle < num_cycles:
        cur_rollers = single_cycle(cubes, cur_rollers, size)
        cur_cycle += 1
        roller_hash = hash(frozenset(cur_rollers))
        if roller_hash in seen_hashes:
            prev_cycle = seen_hashes[roller_hash]
            repeat_diff = cur_cycle - prev_cycle
            print(f'found loop at cycle {cur_cycle} - same as {prev_cycle}, loop length = {repeat_diff}')
            # 3, 9, 20 -> 15
            # 11, 6 -> 6
            cur_cycle += ((num_cycles - cur_cycle) // repeat_diff) * repeat_diff
            print(f'Jumped to {cur_cycle}')
        else:
            seen_hashes[roller_hash] = cur_cycle
    return cur_rollers


def cubes_n_rollers_string(cubes, rollers, dish_size):
    return '\n'.join((
        ''.join(
            (
                '#' if (i, j) in cubes else (
                    'O' if (i, j) in rollers else '.'
                )
            )
            for j in range(dish_size)
        )
        for i in range(dish_size)
    )) + '\n'


def total_load(rollers, dish_size):
    load = 0
    for roller_x, roller_y in rollers:
        load += (dish_size - roller_x)
    return load


def main():
    with open('input/day14_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    cubes, rollers, dish_size = parse_dish(input_lines)
    rolled_north = roll_north(cubes, rollers, dish_size)
    print(total_load(rolled_north, dish_size))
    print(cubes_n_rollers_string(cubes, rolled_north, dish_size))
    print()
    # rollers_cycle = single_cycle(cubes, rollers, dish_size)
    # print(cubes_n_rollers_string(cubes, rollers_cycle, dish_size))
    # rollers_cycle = single_cycle(cubes, rollers_cycle, dish_size)
    # print(cubes_n_rollers_string(cubes, rollers_cycle, dish_size))
    # rollers_cycle = single_cycle(cubes, rollers_cycle, dish_size)
    # print(cubes_n_rollers_string(cubes, rollers_cycle, dish_size))
    print()
    rollers_cycle_alot = repeated_cycle(cubes, rollers, dish_size, 1000000000)
    print(cubes_n_rollers_string(cubes, rollers_cycle_alot, dish_size))
    print(total_load(rollers_cycle_alot, dish_size))


if __name__ == '__main__':
    main()
