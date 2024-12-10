from typing import Dict, List

from utils import DIRECTIONS2, dijkstra_steps, add_coord, A


TEST_INPUT_MINE = '''01234
12345
23456
34567
45678
56789'''

TEST_INPUT = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''

TEST_INPUT_PT2_1 = '''.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
'''

TEST_INPUT_PT2_2 = '''..90..9
...1.98
...2..7
6543456
765.987
876....
987....
'''

TEST_INPUT_PT2_3 = '''012345
123456
234567
345678
4.6789
56789.
'''


def to_upward_neighbor_map(input_lines):
    result = {}
    trailheads = []
    peaks = []
    for i, line in enumerate(input_lines):
        for j, el in enumerate(line.strip()):
            loc = (i, j)
            try:
                height = int(el)
            except ValueError:
                continue
            if height == 0:
                trailheads.append(loc)
            if height == 9:
                peaks.append(loc)
            result[loc] = []
            for direction in DIRECTIONS2:
                ni, nj = add_coord(loc, direction)
                if not (0 <= ni < len(input_lines)):
                    continue
                if not (0 <= nj < len(input_lines[ni].strip())):
                    continue
                try:
                    n_height = int(input_lines[ni][nj])
                except ValueError:
                    continue
                if n_height != height + 1:
                    continue
                result[loc].append((ni, nj))
    return result, trailheads, peaks


def get_trailhead_score(trailhead, upward_map, peaks):
    trail_paths = dijkstra_steps(upward_map, trailhead)
    result = 0
    for peak in peaks:
        if peak in trail_paths:
            result += 1
    return result


def dijkstra_upward_distinctness(graph: Dict[A, List[A]], start: A) -> Dict[A, int]:
    result = {start: 1}
    new = [start]
    while new:
        node = new.pop(0)
        path_count = result[node]
        for neigbor in graph[node]:
            if neigbor not in result:
                new.append(neigbor)
                result[neigbor] = 0
            result[neigbor] += path_count
    return result


def get_trailhead_rating(trailhead, upward_map, peaks):
    distinct_paths = dijkstra_upward_distinctness(upward_map, trailhead)
    result = 0
    for peak in peaks:
        if peak in distinct_paths:
            result += distinct_paths[peak]
    return result


def main():
    test_input = TEST_INPUT.splitlines()
    with open('input/day10.txt') as f:
        test_input = f.readlines()
    upward_map, trailheads, peaks = to_upward_neighbor_map(test_input)
    print(sum((get_trailhead_score(trailhead, upward_map, peaks) for trailhead in trailheads)))
    print(sum((get_trailhead_rating(trailhead, upward_map, peaks) for trailhead in trailheads)))


if __name__ == '__main__':
    main()
