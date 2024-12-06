from utils import DIRECTIONS2, add_coord


TEST_INPUT = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''


CUSTOM_TEST = '''....#...
.....#..
........
....^...
........
........
........
'''


def read_map(input_lines):
    obstacles = set()
    player = None
    x_max = 0
    y_max = 0
    for i, line in enumerate(input_lines):
        if line.strip():
            x_max = i
            y_max = len(line.strip()) - 1
        for j, char in enumerate(line.strip()):
            if char == '#':
                obstacles.add((i, j))
            elif char == '^':
                player = (i, j)
    return obstacles, player, (x_max, y_max)


def is_in_bounds(loc, bounds):
    x, y = loc
    x_max, y_max = bounds
    return 0 <= x <= x_max and 0 <= y <= y_max


def walk_to(player, direction, obstacles, bounds):
    cur_loc = player
    next_loc = add_coord(cur_loc, direction)
    walked_locs = set()
    while next_loc not in obstacles and is_in_bounds(next_loc, bounds):
        cur_loc = next_loc
        walked_locs.add(cur_loc)
        next_loc = add_coord(cur_loc, direction)
    return cur_loc, walked_locs, is_in_bounds(next_loc, bounds)


def print_map(obstacles, walked, bounds):
    x_max, y_max = bounds
    for x in range(0, x_max + 1):
        result = ''.join((
            '#' if (x, y) in obstacles else (
                'X' if (x, y) in walked else '.'
            )
            for y in range(0, y_max + 1)
        ))
        print(result)


def walk_around(player, obstacles, bounds):
    start_direction_idx = 2  # UP2
    walked_locs = {player}
    cur_loc = player
    steps = 0
    while True:
        cur_loc, walked_now, in_bounds = walk_to(cur_loc, DIRECTIONS2[start_direction_idx], obstacles, bounds)
        start_direction_idx = (start_direction_idx - 1) % 4
        walked_locs.update(walked_now)
        steps += 1
        # print_map(obstacles, walked_locs, bounds)
        # print()
        if not in_bounds:
            break
    print(steps)
    return len(walked_locs)


def main():
    test_input = TEST_INPUT.splitlines()
    test_input = CUSTOM_TEST.splitlines()
    with open('input/day06.txt') as f:
        test_input = f.readlines()
    obstacles, player, bounds = read_map(test_input)
    print(walk_around(player, obstacles, bounds))
    # 2619 < result < 5270


if __name__ == '__main__':
    main()
