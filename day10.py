TEST1 = '''-L|F7
7S-7|
L|7||
-L-J|
L|-JF'''

TEST2 = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''

TEST3 = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''

TEST4 = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''

TEST5 = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''


def node_connections(el, i, j, max_len_x, max_len_y):
    result = []

    def add_above():
        if i > 0:
            result.append((i - 1, j))

    def add_below():
        if i < max_len_x - 1:
            result.append((i + 1, j))

    def add_left():
        if j > 0:
            result.append((i, j - 1))

    def add_right():
        if j < max_len_y - 1:
            result.append((i, j + 1))

    if el == '|':
        add_above()
        add_below()
    elif el == '-':
        add_left()
        add_right()
    elif el == 'L':
        add_above()
        add_right()
    elif el == 'J':
        add_above()
        add_left()
    elif el == '7':
        add_left()
        add_below()
    elif el == 'F':
        add_right()
        add_below()
    elif el == 'S':
        add_above()
        add_below()
        add_left()
        add_right()

    return result


def parse_node_map(lines):
    return sanitize_node_map({
        (i, j): node_connections(el, i, j, len(lines), len(lines[0].strip()))
        for i, line in enumerate(lines)
        for j, el in enumerate(line.strip())
    })


def sanitize_node_map(node_map):
    return {
        key: [val for val in value_list if key in node_map[val]]
        for key, value_list in node_map.items()
    }


def find_start(lines):
    return next((
        (i, j)
        for i, line in enumerate(lines)
        for j, el in enumerate(line.strip())
        if el == 'S'
    ))


def follow_path(node_map, initial_path):
    path = list(initial_path)
    last = initial_path[-1]
    while True:
        candidates = [n for n in node_map[last] if n != path[-2]]
        if not candidates:
            return path
        if len(candidates) > 1:
            raise ValueError(path, candidates)
        next_node = candidates[0]
        path.append(next_node)
        last = next_node
        if next_node in path[:-1]:
            return path


def find_loop(node_map, start):
    for second in node_map[start]:
        path = follow_path(node_map, [start, second])
        if path[-1] == path[0]:
            return path


def get_jumps(the_loop):
    # clean_node_map = {
    #     key: [val for val in value if val in the_loop]
    #     for key, value in node_map.items()
    #     if key in the_loop
    # }
    jumps = set()
    for head, tail in zip(the_loop[1:], the_loop[:-1]):
        if head[1] == tail[1]:  # vertical pipe connection
            jump_start_x = min(head[0], tail[0]) + 1
            jumps.add(frozenset({(jump_start_x, head[1]), (jump_start_x, head[1] + 1)}))
        elif head[0] == tail[0]:  # horizontal pipe connection
            jump_start_y = min(head[1], tail[1]) + 1
            jumps.add(frozenset({(head[0], jump_start_y), (head[0] + 1, jump_start_y)}))
    return jumps


def count_jumps_to(node, jumps):
    x, y = node
    count = 0
    for i in range(x):
        if frozenset([(i, 0), (i + 1, 0)]) in jumps:
            count += 1
    for j in range(y):
        if frozenset([(x, j), (x, j + 1)]) in jumps:
            count += 1
    return count


def count_inner(raw_lines, path, jumps):
    ground_locs = [
        (i, j)
        for i, line in enumerate(raw_lines)
        for j, el in enumerate(line)
        if (i, j) not in path
    ]
    total = 0
    for loc in ground_locs:
        jump_count = count_jumps_to(loc, jumps)
        if jump_count % 2 == 1:
            total += 1
    return total


def main():
    with open('input/day10_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST5.splitlines()
    node_map = parse_node_map(input_lines)
    start = find_start(input_lines)
    loop = find_loop(node_map, start)
    print((len(loop) - 1) / 2.0)
    jumps = get_jumps(loop)
    print(count_inner(input_lines, loop, jumps))


if __name__ == '__main__':
    main()
