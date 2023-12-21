TEST = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''


def parse_garden(input_lines):
    walls = [
        (i, j)
        for i, line in enumerate(input_lines)
        for j, el in enumerate(line.strip())
        if el == '#'
    ]
    start = next((
        (i, j)
        for i, line in enumerate(input_lines)
        for j, el in enumerate(line.strip())
        if el == 'S'
    ))
    return start, walls, len(input_lines)


def get_neighbors(pos, walls, to_skip, side_len, wall_len=None):
    if wall_len is None:
        wall_len = side_len
    i, j = pos
    naive_result = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    return [
        (n, m)
        for n, m in naive_result
        if (n % wall_len, m % wall_len) not in walls and
           (n, m) not in to_skip and
           0 <= n < side_len and 0 <= m < side_len
    ]


def get_all_neighbors(positions, walls, to_skip, side_len, wall_len=None):
    result = set()
    for pos in positions:
        result.update(get_neighbors(pos, walls, to_skip, side_len, wall_len=wall_len))
    return result


def get_reachable_in(start_positions, walls, side_len, steps, wall_len=None):
    reachable_in = {0: set(start_positions)}
    result_odd = set()
    result_even = set(start_positions)
    for i in range(1, steps + 1):
        walls_now = result_even if i % 2 == 0 else result_odd
        reachable_in[i] = get_all_neighbors(
            reachable_in[i - 1], walls, walls_now, side_len, wall_len=wall_len
        )
        if i % 2 == 0:
            result_even.update(reachable_in[i])
        else:
            result_odd.update(reachable_in[i])
    if steps % 2 == 0:
        return result_even
    else:
        return result_odd


def main():
    with open('input/day21_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    start, walls, side_len = parse_garden(input_lines)
    print(len(get_reachable_in([start], walls, side_len, 64)))


if __name__ == '__main__':
    main()
