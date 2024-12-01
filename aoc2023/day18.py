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


def find_an_intersecting_edge(min_y, top_x, bot_x, corners):
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
    return the_index


def find_intersecting_edges(min_y, top_x, bot_x, corners):
    index = find_an_intersecting_edge(min_y, top_x, bot_x, corners)
    the_y = corners[index][1]
    result = []
    for j, edge in enumerate(zip(corners[:-1], corners[1:])):
        if edge[0][1] != edge[1][1]:
            continue  # only care about vertical edges
        if edge[0][1] <= min_y:
            continue  # must be to the right
        if line_overlap(top_x, bot_x, edge[0][0], edge[1][0]):
            if edge[0][1] == the_y:
                result.append(j)
    return result


def rotate_corners(corners, i):
    # corner at index i < len(corners) - 1 should be put first
    return corners[i:-1] + corners[:i] + [corners[i]]


def part1(instrs):
    # very slow, but it gets us to part 2
    path = build_loop(instrs)
    jumps = get_jumps(path)

    x_min = min((x for x, y in path))
    x_max = max((x for x, y in path))
    y_min = min((y for x, y in path))
    y_max = max((y for x, y in path))
    ground_locs = [
        (i, j)
        for i in range(x_min - 1, x_max + 2)
        for j in range(y_min - 1, y_max + 2)
    ]
    inner = count_inner(ground_locs, path, jumps, (x_min - 1, y_min - 1))
    print(inner + len(set(path)))  # 38147, too low


def compute_area(corners):
    i, left_edge = get_leftmost_edge(corners)
    corners = rotate_corners(corners, i)
    js = find_intersecting_edges(
        left_edge[0][1], left_edge[0][0], left_edge[1][0], corners
    )
    corner_partitions = []
    intersect_y = corners[js[0]][1]

    my_area = (abs(left_edge[0][0] - left_edge[1][0]) + 1) * (abs(left_edge[0][1] - intersect_y) + 1)

    if js[0] > 2:
        to_append = [(corners[2][0], intersect_y)] + corners[2:js[0] + 1]
        to_append.append(to_append[0])
        corner_partitions.append(to_append)
        overlap_bot = min(to_append[-2][0], left_edge[0][0])
        overlap_top = left_edge[1][0]
        my_area -= (overlap_bot - overlap_top) + 1

    for j, prev in zip(js[1:], js[:-1]):
        corner_partitions.append(
            corners[prev + 1:j + 1] + [corners[prev + 1]]
        )
        overlap_bot = min(corner_partitions[-1][-2][0], left_edge[0][0])
        overlap_top = max(corner_partitions[-1][0][0], left_edge[1][0])
        my_area -= overlap_bot - overlap_top + 1

    if js[-1] + 1 < len(corners) - 2:
        to_append = corners[js[-1] + 1:-1] + [(corners[-2][0], intersect_y)]
        to_append.append(to_append[0])
        corner_partitions.append(to_append)

        overlap_bot = left_edge[0][0]
        overlap_top = max(to_append[0][0], left_edge[1][0])
        my_area -= (overlap_bot - overlap_top) + 1

    total_area = my_area
    for partition in corner_partitions:
        total_area += compute_area(partition)

    return total_area


def main():
    with open('input/day18_input.txt') as f:
        input_lines = f.readlines()
    test_input_lines = TEST.splitlines()
    test2_input_lines = TEST2.splitlines()
    instrs = read_instructions(input_lines)

    # part1(instrs)
    # ^ initial version, very slow
    print(compute_area(get_corners_pt2(instrs, False)))
    print(compute_area(get_corners_pt2(instrs, True)))

    assert compute_area([
        (0, 0), (0, 1), (-1, 1), (-1, 4), (1, 4), (1, 2), (3, 2), (3, 4), (4, 4), (4, 2), (6, 2), (6, 4), (8, 4),
        (8, 3), (7, 3), (7, 0), (0, 0)
    ]) == 42
    assert compute_area([
        (0, 0), (0, 2), (-1, 2), (-1, 4), (1, 4), (1, 2), (3, 2), (3, 4), (4, 4), (4, 2), (6, 2), (6, 4), (8, 4),
        (8, 3), (7, 3), (7, 0), (0, 0)
    ]) == 41
    assert compute_area([
        (0, 0), (0, 2), (-1, 2), (-1, 4), (1, 4), (1, 2), (3, 2), (3, 4), (4, 4), (4, 0), (0, 0)
    ]) == 26
    assert compute_area([
        (0, 0), (0, 2), (-1, 2), (-1, 4), (1, 4), (1, 0), (0, 0)
    ]) == 13
    assert compute_area([
        (0, 0), (0, 3), (-1, 3), (-1, 4), (1, 4), (1, 2), (3, 2), (3, 4), (4, 4), (4, 2), (6, 2), (6, 4), (8, 4),
        (8, 3), (7, 3), (7, 0), (0, 0)
    ]) == 40
    assert compute_area([
        (0, 0), (0, 3), (-1, 3), (-1, 4), (1, 4), (1, 2), (3, 2), (3, 4), (4, 4), (4, 2), (6, 2), (6, 4), (7, 4),
        (7, 0), (0, 0)
    ]) == 38
    assert compute_area([
        (0, 0), (0, 4), (1, 4), (1, 2), (3, 2), (3, 4), (4, 4), (4, 2), (6, 2), (6, 4), (7, 4), (7, 0), (0, 0)
    ]) == 36
    assert compute_area([
        (0, 0), (0, 4), (1, 4), (1, 3), (3, 3), (3, 4), (4, 4), (4, 3), (6, 3), (6, 4), (7, 4), (7, 0), (0, 0)
    ]) == 38
    assert compute_area([
        (0, 0), (0, 4), (1, 4), (1, 3), (3, 3), (3, 4), (4, 4), (4, 3), (5, 3), (5, 0), (0, 0)
    ]) == 28
    assert compute_area(get_corners_pt2(read_instructions(test_input_lines))) == 952408144115
    assert compute_area(get_corners_pt2(read_instructions(test_input_lines), part2=False)) == 62
    assert compute_area(get_corners_pt2(read_instructions(test2_input_lines), part2=False)) == 65
    corners = [(0, 0), (0, 4), (2, 4), (2, 2), (3, 2), (3, 0), (0, 0)]
    assert compute_area(corners) == 18
    corners = [(0, 0), (0, 3), (1, 3), (1, 2), (3, 2), (3, 3), (4, 3), (4, 0), (0, 0)]
    assert compute_area(corners) == 19
    corners = [(0, 0), (0, 6), (1, 6), (1, 2), (3, 2), (3, 6), (4, 6), (4, 0), (0, 0)]
    assert compute_area(corners) == 31


if __name__ == '__main__':
    main()
