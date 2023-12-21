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


def get_neighbors(pos, walls, to_skip, wall_len, min_coord=None, max_coord=None):
    if min_coord is None:
        min_coord = 0
    if max_coord is None:
        max_coord = wall_len
    i, j = pos
    naive_result = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    return [
        (n, m)
        for n, m in naive_result
        if
        (n % wall_len, m % wall_len) not in walls and
        (n, m) not in to_skip and
        min_coord <= n < max_coord and min_coord <= m < max_coord
    ]


def get_all_neighbors(positions, walls, to_skip, wall_len, min_coord=None, max_coord=None):
    result = set()
    for pos in positions:
        result.update(get_neighbors(pos, walls, to_skip, wall_len, min_coord=min_coord, max_coord=max_coord))
    return result


def get_reachable_in(start_positions, walls, wall_len, steps, min_coord=None, max_coord=None):
    reachable_in = {0: set(start_positions)}
    result_odd = set()
    result_even = set(start_positions)
    for i in range(1, steps + 1):
        skip_now = result_even if i % 2 == 0 else result_odd
        reachable_in[i] = get_all_neighbors(
            reachable_in[i - 1], walls, skip_now, wall_len, min_coord=min_coord, max_coord=max_coord
        )
        if not reachable_in[i]:
            break
        skip_now.update(reachable_in[i])
    if steps % 2 == 0:
        return result_even
    else:
        return result_odd


def compute_filled_garden(start_position, walls, wall_len):
    reachable_in = {0: {start_position}}
    result_odd = set()
    result_even = {start_position}
    i = 1
    while True:
        walls_now = result_even if i % 2 == 0 else result_odd
        reachable_in[i] = get_all_neighbors(
            reachable_in[i - 1], walls, walls_now, wall_len
        )
        if not reachable_in[i]:
            break
        if i % 2 == 0:
            result_even.update(reachable_in[i])
        else:
            result_odd.update(reachable_in[i])
        i += 1
    return result_odd, result_even, i - 1


def positions_to_string(positions, walls, wall_len):
    min_x = min((pos[0] for pos in positions))
    max_x = max((pos[0] for pos in positions))
    min_y = min((pos[1] for pos in positions))
    max_y = max((pos[1] for pos in positions))
    return '\n'.join(
        ('\n' if i % wall_len == 0 else '') +
        ''.join(
            (('|' if j % wall_len == 0 else '') +
             ('.' if (i % wall_len, j % wall_len) in walls else (
                'O' if (i, j) in positions else '.'
             )))
            for j in range(min_y, max_y + 1)
        )
        for i in range(min_x, max_x + 1)
    )


def get_positions_in_grid(positions, grid_i, grid_j, side_len):
    return ([
        (i, j)
        for (i, j) in positions if
        (i // side_len == grid_i and j // side_len == grid_j)
    ])


def count_reachable_in_pt2(start, walls, side_len, steps, verbose=False):
    def get_my_reachable_for_big_step(m):
        return get_reachable_in(
            [start], walls, side_len, steps % side_len + m * side_len,
            min_coord=float('-inf'),
            max_coord=float('inf')
        )

    if steps <= 4 * side_len:
        return len(get_my_reachable_for_big_step(steps // side_len))

    # the figure we compute is a quite regular! Check this by printing it for a given number of steps,
    # then also printing it after doing side_len additional steps. Note that the shapes on the x and y axis are
    # exactly the same, but bigger. The shape in the quadrants get 'duplicated'
    # We need to leverage this regularity to compute an efficient result.

    n = 2
    filled_odd, filled_even, filling_steps = compute_filled_garden(start, walls, side_len)
    result_base = 0
    add_per_step = 0
    last_diffs = []
    while True:
        # the shape might be a bit irregular when it is small, so first grow it until its growth is predictable
        # So: compute it explicitly for two consecutive n
        base_steps = get_my_reachable_for_big_step(n)
        next_steps = get_my_reachable_for_big_step(n + 1)
        # add_per_step contains the quadrant pieces. This is a constant number
        add_per_step = (
            len(get_positions_in_grid(base_steps, -1, -1 * n, side_len)) +
            len(get_positions_in_grid(base_steps, -1, -1 * (n - 1), side_len)) +
            len(get_positions_in_grid(base_steps, 1, -1 * n, side_len)) +
            len(get_positions_in_grid(base_steps, 1, -1 * (n - 1), side_len)) +
            len(get_positions_in_grid(base_steps, -1, n, side_len)) +
            len(get_positions_in_grid(base_steps, -1, n - 1, side_len)) +
            len(get_positions_in_grid(base_steps, 1, n, side_len)) +
            len(get_positions_in_grid(base_steps, 1, n - 1, side_len))
        )
        computed_next_steps = (
            len(base_steps) + (2 * n) * len(filled_odd) + (2 * n) * len(filled_even) + add_per_step
        )  # the addition of   ^  this part and              ^ this part
        # is for the interior blocks which get filled. You should check that visually, there are 2 * n  * 2 blocks
        # However, there will be a small estimation error, since I do not know how to predict even/oddness of these
        # blocks, and maybe there is another mistake in the calculation above.
        # The mistake seems to be constant once n is big enough. So we wait for 3 consecutively equal errors,
        # then incorporate that error into our estimate
        last_diffs.append(len(next_steps) - computed_next_steps)
        if verbose:
            print(f'Status: {len(next_steps)} vs {computed_next_steps}, {last_diffs}')
        if len(last_diffs) >= 3 and all((el == last_diffs[-1] for el in last_diffs[-3:])):
            if verbose:
                print(f'Breaking and correcting for {last_diffs[-1]}')
            result_base = len(base_steps)
            add_per_step += last_diffs[-1]
            break
        n += 1
        if n * side_len + steps % side_len == steps:
            if verbose:
                print('Shortcircuiting for small query...')
            return len(next_steps)

    start_n = n

    while n * side_len + steps % side_len < steps:
        result_base += add_per_step
        result_base += (2 * n) * len(filled_odd) + (2 * n) * len(filled_even)
        n += 1
        if start_n + 1 < n <= 6 and verbose:
            print('Checking with slow calculation...')
            result_slow = len(get_my_reachable_for_big_step(n))
            print(f'Steps: {n * side_len + steps % side_len}, fast: {result_base}, slow: {result_slow}')
            if result_slow == result_base:
                print(f'Seems right! :D')
            else:
                print(f'Seems WRONG! :(')
    return result_base


def main():
    with open('input/day21_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    start, walls, side_len = parse_garden(input_lines)
    print(len(get_reachable_in([start], walls, side_len, 64)))
    # print(count_reachable_in_pt2(start, walls, side_len, 10))
    # print(count_reachable_in_pt2(start, walls, side_len, 50))
    # print(count_reachable_in_pt2(start, walls, side_len, 100))
    # print(count_reachable_in_pt2(start, walls, side_len, 500))
    # print(count_reachable_in_pt2(start, walls, side_len, 1000))
    # print(count_reachable_in_pt2(start, walls, side_len, 5000))
    print(count_reachable_in_pt2(start, walls, side_len, 26501365, verbose=True))


if __name__ == '__main__':
    main()
