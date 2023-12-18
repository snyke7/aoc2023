from day10 import get_jumps, count_inner

TEST = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''  # area: 62

TEST2 = '''R 6 (#70c710)
D 4 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 3 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 2 (#1b58a2)
U 2 (#caa171)
R 3 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''  # area: 65

TEST3 = '''R 5 (#70c710)
D 1 (#70c710)
R 2 (#70c710)
D 4 (#70c710)
L 2 (#70c710)
U 2 (#70c710)
L 2 (#70c710)
D 2 (#70c710)
L 2 (#70c710)
U 2 (#70c710)
L 1 (#70c710)
U 3 (#70c710)'''


def read_instructions(input_lines):
    return [
        (
            line.split(' ')[0],
            int(line.split(' ')[1]),
            (
                int(line.strip().split(' ')[2][-2]),
                int(line.strip().split(' ')[2][2:-2], 16)
            )
        )
        for line in input_lines
    ]


HEADING_DIRECTION_MAP = {
    'R': 0,
    'D': 1,
    'L': 2,
    'U': 3
}


def direction_to_dpos(direction):
    dy, dx = (1 - direction) if direction % 2 == 0 else 0, (2 - direction) if direction % 2 == 1 else 0
    return dx, dy


def build_loop(instructions):
    cur_x, cur_y = (0, 0)
    result = [(cur_x, cur_y)]
    for heading, amnt, _ in instructions:
        dx, dy = direction_to_dpos(HEADING_DIRECTION_MAP[heading])
        for i in range(amnt):
            cur_x += dx
            cur_y += dy
            result.append((cur_x, cur_y))
    return result


def part1(instrs):
    path = build_loop(instrs)
    jumps = get_jumps(path)
    print(len(path))
    print(len(set(path)))

    x_min = min((x for x, y in path))
    x_max = max((x for x, y in path))
    y_min = min((y for x, y in path))
    y_max = max((y for x, y in path))
    print(x_min, x_max)
    print(y_min, y_max)
    ground_locs = [
        (i, j)
        for i in range(x_min - 1, x_max + 2)
        for j in range(y_min - 1, y_max + 2)
    ]
    inner = count_inner(ground_locs, path, jumps, (x_min - 1, y_min - 1))
    print(inner)
    print(inner + len(set(path)))  # 38147, too low


def get_corners_pt2(instrs, part2=True):
    if part2:
        return get_corners([(direction, amnt) for _, _, (direction, amnt) in instrs])
    else:
        return get_corners([(HEADING_DIRECTION_MAP[heading], amnt) for heading, amnt, _ in instrs])


def get_corners(instrs):
    cur_x, cur_y = (0, 0)
    result = [(cur_x, cur_y)]
    for direction, amnt in instrs:
        dx, dy = direction_to_dpos(direction)
        cur_x += amnt * dx
        cur_y += amnt * dy
        result.append((cur_x, cur_y))
    return result


def get_leftmost_edge(corners):
    leftest = min((y for x, y in corners))
    for i, ((cur_x, cur_y), (next_x, next_y)) in enumerate(zip(corners[:-1], corners[1:])):
        if cur_y != leftest or next_y != leftest:
            continue
        return i, ((cur_x, cur_y), (next_x, next_y))


def line_overlap(line1_l, line1_r, line2_l, line2_r):
    return line_overlap_min_max(
        min(line1_l, line1_r),
        max(line1_l, line1_r),
        min(line2_l, line2_r),
        max(line2_l, line2_r),
    )


def line_overlap_min_max(line1_min, line1_max, line2_min, line2_max):
    return line2_min <= line1_max and line1_min <= line2_max


def find_intersecting_edge(min_y, top_x, bot_x, corners):
    dist_y = float('inf')
    the_index = None
    for j, edge in enumerate(zip(corners[:-1], corners[1:])):
        if edge[0][1] != edge[1][1]:
            continue  # only care about vertical edges
        if edge[0][1] <= min_y:
            continue  # must be to the right
        if line_overlap(top_x, bot_x, edge[0][0], edge[1][0]):
            this_dist = edge[0][1] - min_y
            if this_dist < dist_y:
                dist_y = this_dist
                the_index = j
    if the_index is None:
        print(f'faulty corners: {corners}')
        print(f'wrt: {min_y, top_x, bot_x}')
    return the_index, (corners[the_index], corners[the_index + 1])


def compute_area(corners):
    i, left_edge = get_leftmost_edge(corners)
    j, intersecting_edge = find_intersecting_edge(
        left_edge[0][1], left_edge[0][0], left_edge[1][0], corners
    )
    if i == len(corners) - 2:
        bot_corners = corners[j + 2:i]
        top_corners = corners[1:j]
    elif i > j:
        bot_corners = corners[j + 2:i]
        top_corners = corners[i + 2:-1] + corners[:j]
        if len(top_corners) == 1:
            top_corners = []
    else:
        top_corners = corners[i + 2:j]
        bot_corners = corners[j + 2:-1] + corners[:i]
        if len(bot_corners) == 1:
            bot_corners = []

    my_area = (abs(left_edge[0][0] - left_edge[1][0]) + 1) * (abs(left_edge[0][1] - intersecting_edge[0][1]) + 1)
    if (i + 2) % (len(corners) - 1) == j or (i - 2) % (len(corners) - 1) == j:
        if top_corners or bot_corners:
            my_area -= (intersecting_edge[0][0] - left_edge[1][0] + 1)
    else:
        assert top_corners
        assert bot_corners
        my_area -= (intersecting_edge[0][0] - left_edge[1][0] + 1)
        my_area -= (left_edge[0][0] - intersecting_edge[1][0] + 1)
    print(my_area, left_edge, intersecting_edge)

    total_area = my_area
    if bot_corners:
        # subtracted_horiz_line = False
        # total_area -= (intersecting_edge[1][1] - bot_corners[-1][1]) + 1
        # subtracted_horiz_line = True
        if intersecting_edge[1][0] != left_edge[0][0]:
            # if intersecting_edge[1][0] < left_edge[0][0]:
            #     total_area -= (left_edge[0][0] - intersecting_edge[1][0] + 1)
            #     if subtracted_horiz_line:
            #         total_area += 1
            bot_corners.append((bot_corners[-1][0], intersecting_edge[1][1]))
            bot_corners.append(intersecting_edge[1])
        print(f'minus overlapping bot: {total_area}')
        bot_corners.append(bot_corners[0])
        print(f'bottom: {bot_corners}')
        print(f'all: {corners}')
        print(f'left, intersect: {left_edge, intersecting_edge} at {i, j, len(corners)}')
        total_area += compute_area(bot_corners)

    if top_corners:
        # subtracted_horiz_line = False
        # total_area -= (intersecting_edge[0][1] - top_corners[0][1]) + 1
        # subtracted_horiz_line = True
        if intersecting_edge[0][0] != left_edge[1][0]:
            # if intersecting_edge[0][0] > left_edge[1][0]:
            #     total_area -= (intersecting_edge[0][0] - left_edge[1][0] + 1)
            #     if subtracted_horiz_line:
            #         total_area += 1
            # total_area -= abs(intersecting_edge[0][0] - left_edge[1][0])
            top_corners.append(intersecting_edge[0])
            top_corners.append((top_corners[0][0], intersecting_edge[0][1]))
        top_corners.append(top_corners[0])
        print(f'minus overlapping top: {total_area}')
        print(f'top: {top_corners}')
        print(f'all: {corners}')
        print(f'left, intersect: {left_edge, intersecting_edge} at {i, j, len(corners)}')
        total_area += compute_area(top_corners)

    print(f'returning: {total_area}')
    return total_area


def main():
    with open('input/day18_input.txt') as f:
        input_lines = f.readlines()
    input_lines = TEST2.splitlines()
    instrs = read_instructions(input_lines)
    corners = get_corners_pt2(instrs, part2=False)
    # print(compute_area(corners))

    corners = [(0, 0), (0, 4), (2, 4), (2, 2), (3, 2), (3, 0), (0, 0)]
    assert compute_area(corners) == 18
    #
    # corners = [(4, 4), (5, 4), (5, 2), (2, 2), (2, 3), (1, 3), (1, 6), (4, 6), (4, 4)]
    # print(compute_area(corners))
    #
    # corners = [(4, 4), (5, 4), (5, 2), (2, 2), (2, 4), (3, 4), (3, 6), (4, 6), (4, 4)]
    # print(compute_area(corners))

    print()
    corners = [(0, 0), (0, 3), (1, 3), (1, 2), (3, 2), (3, 3), (4, 3), (4, 0), (0, 0)]
    assert compute_area(corners) == 19
    print()
    corners = [(0, 0), (0, 6), (1, 6), (1, 2), (3, 2), (3, 6), (4, 6), (4, 0), (0, 0)]
    assert compute_area(corners) == 31

    # corners = [(0, 4), (0, 6), (4, 6), (4, 4), (2, 4), (2, 2), (4, 2), (4, 0), (2, 0), (2, 4), (0, 4)]
    # print(corners)
    # print(compute_area(corners))
    # print()
    #
    # corners = [(0, 3), (0, 6), (4, 6), (4, 4), (2, 4), (2, 2), (4, 2), (4, 0), (2, 0), (2, 3), (0, 3)]
    # print(corners)
    # print(compute_area(corners))
    # print()
    #
    # corners = [(0, 2), (0, 6), (4, 6), (4, 4), (2, 4), (2, 2), (4, 2), (4, 0), (2, 0), (2, 2), (0, 2)]
    # print(corners)
    # print(compute_area(corners))
    # print()
    #
    # corners = [(0, 1), (0, 6), (4, 6), (4, 4), (2, 4), (2, 2), (4, 2), (4, 0), (2, 0), (2, 1), (0, 1)]
    # print(corners)
    # print(compute_area(corners))
    # print()


if __name__ == '__main__':
    main()
