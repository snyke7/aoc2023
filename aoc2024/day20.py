from utils import DIRECTIONS2, add_coord, dijkstra_steps_path


TEST_INPUT = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''


def read_graph(input_lines):
    result = {}
    start = None
    end = None
    for i, line in enumerate(input_lines):
        for j, el in enumerate(line.strip()):
            if el == '#':
                continue
            if el == 'S':
                start = (i, j)
            if el == 'E':
                end = (i, j)
            for k, direction in enumerate(DIRECTIONS2):
                ni, nj = add_coord((i, j), direction)
                if input_lines[ni][nj] != '#':
                    if (i, j) not in result:
                        result[(i, j)] = []
                    result[(i, j)].append(
                        (ni, nj)
                    )
    return result, start, end


def mul_coord(coord, m):
    return tuple(map(lambda c: c * m, coord))


TWO_STEPS = {
    add_coord(the_dir, the_dir)
    for the_dir in DIRECTIONS2
}

AT_MOST_TWENTY_STEPS = {
    add_coord(
        mul_coord(base_dir, num_steps),
        mul_coord(
            add_coord(DIRECTIONS2[(dir_idx + 1) % 4], DIRECTIONS2[(dir_idx + 2) % 4]),
            side_idx
        )
    )
    for num_steps in range(2, 20 + 1)
    for dir_idx, base_dir in enumerate(DIRECTIONS2)
    for side_idx in range(num_steps)
}


def get_cheats(node_map, minimum_save):
    result = {}
    for node, node_idx in node_map.items():
        for step in TWO_STEPS:
            cheat_dest = add_coord(node, step)
            if cheat_dest not in node_map:
                continue
            cheat_idx = node_map[cheat_dest]
            saved_time = cheat_idx - (node_idx + 2)
            if saved_time >= minimum_save:
                if saved_time not in result:
                    result[saved_time] = []
                result[saved_time].append((node, cheat_dest))
    return result


def get_cheats_pt2(node_map, minimum_save):
    result = {}
    for node, node_idx in node_map.items():
        for step in AT_MOST_TWENTY_STEPS:
            cheat_dest = add_coord(node, step)
            if cheat_dest not in node_map:
                continue
            cheat_idx = node_map[cheat_dest]
            cheat_time = sum(map(abs, step))
            saved_time = cheat_idx - (node_idx + cheat_time)
            if saved_time >= minimum_save:
                if saved_time not in result:
                    result[saved_time] = []
                result[saved_time].append((node, cheat_dest))
    return result

def main():
    test_input, pt1_min_save, pt2_min_save = TEST_INPUT.splitlines(), 2, 50
    with open('input/day20.txt') as f:
        test_input, pt1_min_save, pt2_min_save = f.readlines(), 100, 100
    graph, start, end = read_graph(test_input)
    paths = dijkstra_steps_path(graph, start)
    dist_map = {}
    node_map = {}
    _, end_path = paths[end]
    for node, (dist, path) in paths.items():
        if dist in dist_map:
            raise ValueError
        dist_map[dist] = node
        node_map[node] = dist
        if end_path.index(node) != dist:
            raise ValueError
    cheat_map = get_cheats(node_map, pt1_min_save)
    result = 0
    for saved_time in sorted(cheat_map.keys()):
        # print(f'{saved_time}: {len(cheat_map[saved_time])}')
        result += len(cheat_map[saved_time])
    print(result)

    cheat_map_pt2 = get_cheats_pt2(node_map, pt2_min_save)
    result = 0
    for saved_time in sorted(cheat_map_pt2.keys()):
        # print(f'{saved_time}: {len(cheat_map_pt2[saved_time])}')
        result += len(cheat_map_pt2[saved_time])
    print(result)



if __name__ == '__main__':
    main()
