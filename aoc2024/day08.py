from day06 import is_in_bounds
from utils import add_coord, sub_coord


TEST_INPUT = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............'''


def gather_antennas(input_lines):
    antenna_dict = {}
    x_max, y_max = 0, 0
    for i, line in enumerate(input_lines):
        for j, char in enumerate(line.strip()):
            x_max, y_max = i, j
            if char == '.':
                continue
            if char not in antenna_dict:
                antenna_dict[char] = []
            antenna_dict[char].append((i, j))
    return antenna_dict, (x_max, y_max)


def get_antinodes_within_bounds(nodes, bounds, part2=False):
    result = []
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if i == j:
                continue
            diff = sub_coord(node1, node2)
            if not part2:
                antinode = add_coord(node1, diff)
                if is_in_bounds(antinode, bounds):
                    result.append(antinode)
            else:
                antinode = node1
                while is_in_bounds(antinode, bounds):
                    result.append(antinode)
                    antinode = add_coord(antinode, diff)
    return result


def get_all_antinodes_within_bounds(antenna_dict, bounds, part2=False):
    result = set()
    for nodes in antenna_dict.values():
        result.update(get_antinodes_within_bounds(nodes, bounds, part2=part2))
    return result


def main():
    test_input = TEST_INPUT.splitlines()
    with open('input/day08.txt') as f:
        test_input = f.readlines()
    antenna_dict, bounds = gather_antennas(test_input)
    print(len(get_all_antinodes_within_bounds(antenna_dict, bounds)))
    print(len(get_all_antinodes_within_bounds(antenna_dict, bounds, part2=True)))


if __name__ == '__main__':
    main()
