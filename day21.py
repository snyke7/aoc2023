from utils import dijkstra_steps


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


def get_neighbors(pos, walls, to_skip, wall_len, min_coord=None, max_coord=None, grid_skip=None):
    if min_coord is None:
        min_coord = 0
    if max_coord is None:
        max_coord = wall_len
    if grid_skip is None:
        grid_skip = set()
    i, j = pos
    naive_result = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    return [
        (n, m)
        for n, m in naive_result
        if
        (n % wall_len, m % wall_len) not in walls and
        (n, m) not in to_skip and
        (
            (n // wall_len, m // wall_len) not in grid_skip or (
                grid_skip[(n // wall_len, m // wall_len)] is not True and
                (n % wall_len, m % wall_len) not in grid_skip[(n // wall_len, m // wall_len)]
            )
        ) and
        min_coord <= n < max_coord and min_coord <= m < max_coord
    ]


def get_all_neighbors(positions, walls, to_skip, wall_len, min_coord=None, max_coord=None, grid_skip=None):
    result = set()
    for pos in positions:
        result.update(get_neighbors(pos, walls, to_skip, wall_len,
                                    min_coord=min_coord, max_coord=max_coord, grid_skip=grid_skip))
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


def get_origin_step_neighbors(i, j):
    if i == 0:
        if j == 0:
            return []
        return [(0, j - 1)] if j > 0 else [(0, j + 1)]
    else:
        prev_i = i - 1 if i > 0 else i + 1
        if j == 0:
            return [(prev_i, 0)]
        prev_j = j - 1 if j > 0 else j + 1
        return ([(i, prev_j)] if prev_j != 0 else []) + (
            [(prev_i, j)] if prev_i != 0 else []
        )


def get_origin_step_base(i, j):
    if i == 0:
        return (0, j - 1) if j > 0 else ((0, j + 1) if j < 0 else None)
    else:
        if j == 0:
            return (i - 1, 0) if i > 0 else (i + 1, 0)
        return (1 if i > 0 else -1), (1 if j > 0 else -1)


def get_grid_entry_predictor(base_points, wall_len):
    x_min = min((pos[0] for pos in base_points if pos[1] == 0))
    x_max = max((pos[0] for pos in base_points if pos[1] == 0))
    y_min = min((pos[1] for pos in base_points if pos[0] == 0))
    y_max = max((pos[1] for pos in base_points if pos[0] == 0))

    def get_base_point(grid_pos):
        grid_i, grid_j = grid_pos
        base_point = get_origin_step_base(grid_i, grid_j)
        if base_point is None:  # origin
            return None
        if base_point in base_points:
            # probably lies in a quadrant
            return base_point
        else:
            # should lie on a line
            if grid_i == 0:
                if grid_j <= y_min:
                    return 0, y_min
                elif grid_j >= y_max:
                    return 0, y_max
                else:
                    return None
            elif grid_j == 0:
                if grid_i <= x_min:
                    return x_min, 0
                elif grid_i >= x_max:
                    return x_max, 0
                else:
                    return None
            else:
                raise ValueError(base_points, grid_pos)

    def predict_grid_arrival(grid_pos):
        grid_i, grid_j = grid_pos
        base_point = get_base_point(grid_pos)
        if base_point is None:
            return None, []
        dist_to_start = base_points[base_point][0]
        return (
            dist_to_start + (abs(base_point[0] - grid_i) + abs(base_point[1] - grid_j)) * wall_len,
            base_points[base_point][1]
        )

    return predict_grid_arrival, get_base_point


def count_reachable_in_pt2(start_position, walls, wall_len, steps):
    # first calculate how a 'filled' single map looks
    filled_odd, filled_even, filling_steps = compute_filled_garden(start_position, walls, wall_len)
    if steps < filling_steps * 10:
        print(f'Are you testing? Filling steps = {filling_steps}, required = {steps}')
    reachable_in = {0: {start_position}}
    grid_odd = {}
    grid_even = {}
    grid_first_visit = {(0, 0): (0, start_position, [])}
    neighbor_map = {
        (i, j): get_neighbors((i, j), walls, set(), wall_len)
        for i in range(wall_len)
        for j in range(wall_len)
        if (i, j) not in walls
    }
    distance_map = {start_position: dijkstra_steps(neighbor_map, start_position)}
    arrival_base_points = {}
    for i in range(1, steps + 1):
        grid_now = grid_even if i % 2 == 0 else grid_odd
        reachable_in[i] = get_all_neighbors(
            reachable_in[i - 1], walls, {}, wall_len,
            min_coord=float('-inf'), max_coord=float('inf'), grid_skip=grid_now
        )
        cur_filled = filled_even if i % 2 == 0 else filled_odd
        grids_to_remove = set()
        for new_el_x, new_el_y in reachable_in[i]:
            grid_i = new_el_x // wall_len
            grid_j = new_el_y // wall_len
            new_wall_pos = (new_el_x % wall_len, new_el_y % wall_len)
            if (grid_i, grid_j) not in grid_now:
                grid_now[(grid_i, grid_j)] = set()
            if (grid_i, grid_j) not in grid_first_visit:
                the_neighbors = get_origin_step_neighbors(grid_i, grid_j)
                grid_first_visit[(grid_i, grid_j)] = (i, new_wall_pos, [
                    (i - grid_first_visit[neighbor][0], neighbor)
                    for neighbor in the_neighbors
                ])
                if new_wall_pos not in distance_map:
                    distance_map[new_wall_pos] = dijkstra_steps(neighbor_map, new_wall_pos)
                if the_neighbors and all((
                    i - grid_first_visit[origin_neighbor][0] == wall_len
                    for origin_neighbor in the_neighbors
                )):
                    print(f'Found regularity for grid {grid_i, grid_j}')
                    base_coord = get_origin_step_base(grid_i, grid_j)
                    arrival_base_points[base_coord] = tuple(list(grid_first_visit[base_coord])[:2])
            else:
                # check that the reached tile is close to the first one, and otherwise store it as an entrypoint
                old_steps, (old_el_x, old_el_y), _ = grid_first_visit[(grid_i, grid_j)]
                old_to_new = distance_map[(old_el_x, old_el_y)][new_wall_pos]
                if old_to_new + old_steps > i:
                    print(f'Found additional entry point to {grid_i, grid_j}: '
                          f'{new_wall_pos} in {i} steps (< {old_to_new} + {old_steps} from {old_el_x, old_el_y} )')
            grid_now[(grid_i, grid_j)].add((new_el_x % wall_len, new_el_y % wall_len))
            if len(grid_now[(grid_i, grid_j)]) == len(cur_filled):
                grids_to_remove.add((grid_i, grid_j))
        for grid_i, grid_j in grids_to_remove:
            grid_now[(grid_i, grid_j)] = True
        if len(arrival_base_points) == 8:
            print(f'Quitting, enough info for extrapolation: {arrival_base_points}')
            break

    # cur_grid = grid_even if steps % 2 == 0 else grid_odd
    # cur_filled = filled_even if steps % 2 == 0 else filled_odd
    #
    # num_full_grids = sum((1 for val in cur_grid.values() if val is True))
    # partial_plots = sum((len(val) for val in cur_grid.values() if val is not True))
    # print(len(grid_even), num_full_grids)
    # return partial_plots + len(cur_filled) * num_full_grids

    entry_predictor, get_base_point = get_grid_entry_predictor(arrival_base_points, wall_len)
    for grid_pos, (steps, arrive_pos, neighbor_dists) in grid_first_visit.items():
        print(f'Grid: {grid_pos} arrive info: {steps, entry_predictor(grid_pos)[0], arrive_pos, neighbor_dists}')

    longest_internal_dist = (max((
        max(distance_map[internal_coord].values())
        for grid_coord, (steps, internal_coord) in arrival_base_points.items()
    )))  # is always 2 * wall_len, to go from bot_left to top_right. there is no internal maze

    ypos_base = get_base_point((0, 999))
    yneg_base = get_base_point((0, -999))
    xpos_base = get_base_point((999, 0))
    xneg_base = get_base_point((-999, 0))
    result_base = get_reachable_in([start_position], walls, wall_len, steps,
                              min_coord=min(
                                  yneg_base[1] * wall_len + arrival_base_points[yneg_base][1][1],
                                  xneg_base[0] * wall_len + arrival_base_points[xneg_base][1][0]
                              ) + 1,
                              max_coord=max(
                                  ypos_base[1] * wall_len + arrival_base_points[yneg_base][1][1],
                                  xpos_base[0] * wall_len + arrival_base_points[xneg_base][1][0]
                              ) + 1)
    print(result_base)
    result = set([
        (i // wall_len, j // wall_len)
        for (i, j) in result_base if
        (i // wall_len == 0 and yneg_base[1] < j // wall_len < ypos_base[1]) or
        (j // wall_len == 0 and xneg_base[0] < i // wall_len < xpos_base[0])
    ])  # only care about results in the +
    print(result)
    print(xneg_base, xpos_base)
    print(yneg_base, ypos_base)

    # big_ypos_steps = (steps - arrival_base_points[][0]) // wall_len - 2
    # result +=


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


def count_reachable_in_pt3(start, walls, side_len, steps):
    if steps <= 4 * side_len:
        return len(get_reachable_in([start], walls, side_len, steps))

    def get_my_reachable_for_big_step(m):
        return get_reachable_in(
            [start], walls, side_len, steps % side_len + m * side_len,
            min_coord=float('-inf'),
            max_coord=float('inf')
        )

    n = 2
    filled_odd, filled_even, filling_steps = compute_filled_garden(start, walls, side_len)
    result_base = 0
    add_per_step = 0
    while True:
        base_steps = get_my_reachable_for_big_step(n)
        next_steps = get_my_reachable_for_big_step(n + 1)
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
            len(base_steps) + (2 * n + 1) * len(filled_odd) + (2 * n - 1) * len(filled_even) + add_per_step
        )
        if len(next_steps) == computed_next_steps:
            result_base = len(base_steps)
            break
        else:
            print(f'Not yet, {len(next_steps)} vs {computed_next_steps}')
        n += 1

    while n * side_len + steps % side_len < steps:
        result_base += add_per_step
        result_base += (2 * n + 1) * len(filled_odd) + (2 * n - 1) * len(filled_even)
        n += 1
        if n <= 6:
            print(n * side_len + steps % side_len, result_base)
            print(f'Check: {len(get_my_reachable_for_big_step(n))}')
    return result_base

    # base_steps = get_reachable_in(
    #     [start], walls, side_len, steps % side_len + 3 * side_len,
    #     min_coord=float('-inf'),
    #     max_coord=float('inf')
    # )  # between 2 * and 3 * steps
    # print(positions_to_string(base_steps, walls, side_len))
    #
    # limited_steps = get_reachable_in(
    #     [start], walls, side_len, steps % side_len + 4 * side_len,
    #     min_coord=float('-inf'),
    #     max_coord=float('inf')
    # )  # between 2 * and 3 * steps
    # print(positions_to_string(limited_steps, walls, side_len))
    #
    # filled_odd, filled_even, filling_steps = compute_filled_garden(start, walls, side_len)
    # top_left_quadrant = get_positions_in_grid(base_steps, -1, -2, side_len)
    # top_left_quadrant2 = get_positions_in_grid(base_steps, -1, -3, side_len)
    # print(positions_to_string(top_left_quadrant, walls, side_len))
    #
    # print(len(limited_steps))
    # print(len(base_steps) + 7 * len(filled_odd) + 5 * len(filled_even) +
    #       len(top_left_quadrant) +
    #       len(top_left_quadrant2) +
    #       len(get_positions_in_grid(base_steps, 1, -2, side_len)) +
    #       len(get_positions_in_grid(base_steps, 1, -3, side_len)) +
    #       len(get_positions_in_grid(base_steps, -1, 2, side_len)) +
    #       len(get_positions_in_grid(base_steps, -1, 3, side_len)) +
    #       len(get_positions_in_grid(base_steps, 1, 2, side_len)) +
    #       len(get_positions_in_grid(base_steps, 1, 3, side_len))
    # )
    #
    # limited_steps2 = get_reachable_in(
    #     [start], walls, side_len, steps % side_len + 5 * side_len,
    #     min_coord=float('-inf'),
    #     max_coord=float('inf')
    # )  # between 2 * and 3 * steps
    # print(positions_to_string(limited_steps, walls, side_len))
    #
    # filled_odd, filled_even, filling_steps = compute_filled_garden(start, walls, side_len)
    # top_left_quadrant = get_positions_in_grid(base_steps, -1, -2, side_len)
    # top_left_quadrant2 = get_positions_in_grid(base_steps, -1, -3, side_len)
    # print(positions_to_string(top_left_quadrant, walls, side_len))
    # # print(positions_to_string(top_left_quadrant2, walls, side_len))
    #
    # print(len(limited_steps2))
    # print(len(limited_steps) + 9 * len(filled_odd) + 7 * len(filled_even) + len(top_left_quadrant) +
    #       len(top_left_quadrant2) +
    #       len(get_positions_in_grid(base_steps, 1, -2, side_len)) +
    #       len(get_positions_in_grid(base_steps, 1, -3, side_len)) +
    #       len(get_positions_in_grid(base_steps, -1, 2, side_len)) +
    #       len(get_positions_in_grid(base_steps, -1, 3, side_len)) +
    #       len(get_positions_in_grid(base_steps, 1, 2, side_len)) +
    #       len(get_positions_in_grid(base_steps, 1, 3, side_len))
    # )


def main():
    with open('input/day21_input.txt') as f:
        input_lines = f.readlines()
    input_lines = TEST.splitlines()
    # real input has open line in the center! that makes it easier... the test input is harder in that sense
    start, walls, side_len = parse_garden(input_lines)
    print(len(get_reachable_in([start], walls, side_len, 64)))

    print(len(get_reachable_in([start], walls, side_len, 6)))
    print(len(get_reachable_in([start], walls, side_len, 400, float('-inf'), float('inf'))))
    print(count_reachable_in_pt3(start, walls, side_len, 400))
    print(side_len)

    # print([i for i in range(1, side_len - 1) if not any((i, j) in walls for j in range(1, side_len - 1))])
    # print([i for i in range(1, side_len - 1) if not any((j, i) in walls for j in range(1, side_len - 1))])


if __name__ == '__main__':
    main()
