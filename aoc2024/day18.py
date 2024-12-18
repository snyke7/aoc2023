from utils import dijkstra_steps, DIRECTIONS2, add_coord


TEST_INPUT = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''


def build_graph(byte_lines, side_length):
    byte_locs = [tuple(map(int, reversed(byte_line.split(',')))) for byte_line in byte_lines]
    the_map = {(i, j) for i in range(side_length) for j in range(side_length) if (i, j) not in byte_locs}
    return {
        coord: [
            add_coord(coord, direction)
            for direction in DIRECTIONS2
            if add_coord(coord, direction) in the_map
        ]
        for coord in the_map
    }


def get_shortest_path_to_exit(byte_lines, side_length):
    neighbors = build_graph(byte_lines, side_length)
    sp = dijkstra_steps(neighbors, (0, 0))
    end = (side_length - 1, side_length - 1)
    if end in sp:
        return sp[end]
    else:
        return None

def find_cutoff_byte_binary_search(byte_lines, side_length):
    lb = 0
    ub = len(byte_lines)
    while lb + 1 < ub:
        med = (lb + ub) // 2
        sp = get_shortest_path_to_exit(byte_lines[:med], side_length)
        if sp is None:
            ub = med
        else:
            lb = med
    return byte_lines[ub - 1].strip()


def main():
    test_input, side_length = TEST_INPUT.splitlines()[:12], 7
    with open('input/day18.txt') as f:
        test_input, side_length = f.readlines(), 70 + 1
    print(get_shortest_path_to_exit(test_input[:1024], side_length))
    print(find_cutoff_byte_binary_search(test_input, side_length))


if __name__ == '__main__':
    main()
