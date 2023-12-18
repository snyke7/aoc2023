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
U 2 (#7a21e3)'''


def read_instructions(input_lines):
    return [
        (
            line.split(' ')[0],
            int(line.split(' ')[1]),
            int(line.strip().split(' ')[2][2:-1], 16)
        )
        for line in input_lines
    ]


HEADING_DIRECTION_MAP = {
    'R': 0,
    'D': 1,
    'L': 2,
    'U': 3
}


def heading_to_dpos(heading):
    direction = HEADING_DIRECTION_MAP[heading]
    dy, dx = (1 - direction) if direction % 2 == 0 else 0, (2 - direction) if direction % 2 == 1 else 0
    return dx, dy


def build_loop(instructions):
    cur_x, cur_y = (0, 0)
    result = [(cur_x, cur_y)]
    for heading, amnt, _ in instructions:
        dx, dy = heading_to_dpos(heading)
        for i in range(amnt):
            cur_x += dx
            cur_y += dy
            result.append((cur_x, cur_y))
    return result


def main():
    with open('input/day18_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    instrs = read_instructions(input_lines)
    # print(instrs)
    path = build_loop(instrs)
    # print(path)
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


if __name__ == '__main__':
    main()
