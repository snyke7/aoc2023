from typing import TypeVar, Dict, List, Tuple, Optional
from collections import defaultdict


TEST = '''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''


def parse_graph(maze_lines, uphill=False):
    result = {}
    for i, line in enumerate(maze_lines):
        for j, el in enumerate(line.strip()):
            if el == '#':
                continue
            neighbors = []
            if (el in '<.' or uphill) and j > 0 and line[j - 1] != '#':
                neighbors.append((i, j - 1))
            if (el in '>.' or uphill) and j < len(line.strip()) - 1 and line[j + 1] != '#':
                neighbors.append((i, j + 1))
            if (el in '^.' or uphill) and i > 0 and maze_lines[i - 1].strip()[j] != '#':
                neighbors.append((i - 1, j))
            if (el in 'v.' or uphill) and i < len(maze_lines) - 1 and maze_lines[i + 1].strip()[j] != '#':
                neighbors.append((i + 1, j))
            result[(i, j)] = neighbors
    return result


A = TypeVar('A')


def dijkstra_longest(graph: Dict[A, List[A]], start: A, end: Optional[A] = None) -> Dict[A, Dict[A, List[A]]]:
    result = {start: defaultdict(lambda: [start])}
    new_paths = [[start]]
    time = 0
    while new_paths:
        new_path = new_paths.pop(0)
        if time % 10000 == 9999:
            print(time, len(new_paths))
            if end is not None and end in result:
                print(len(result[end]))
        prev = new_path[-1]
        for neighbor in graph[prev]:
            if neighbor not in new_path:
                should_follow = neighbor not in result or len(result[neighbor]) < len(new_path) + 1
                # but more can happen: two paths can go in the opposite direction!
                if not should_follow:
                    should_follow = should_follow or result[neighbor][-1] != new_path[-1]
                if should_follow:
                    result[neighbor] = new_path + [neighbor]
                    new_paths.append(new_path + [neighbor])
        time += 1
    return result


def path_to_str(the_path):
    x_min = min((x for x, _ in the_path))
    x_max = max((x for x, _ in the_path))
    y_min = min((y for _, y in the_path))
    y_max = max((y for _, y in the_path))
    return '\n'.join((
        ''.join((
            'O' if (x, y) in the_path else ' '
            for y in range(y_min, y_max + 1)
        ))
        for x in range(x_min, x_max + 1)
    ))


def main():
    with open('input/day23_input.txt') as f:
        input_lines = f.readlines()
    input_lines = TEST.splitlines()
    start = (0, 1)
    end = (len(input_lines) - 1, len(input_lines[-1].strip()) - 2)

    graph_pt1 = parse_graph(input_lines)
    long_path1 = dijkstra_longest(graph_pt1, start)
    print(len(long_path1[end]) - 1)

    graph_pt2 = parse_graph(input_lines, uphill=True)
    long_path2 = dijkstra_longest(graph_pt2, start, end)
    print(long_path2[end])
    print(path_to_str(long_path2[end]))
    print(len(long_path2[end]) - 1)  # > 4650


if __name__ == '__main__':
    main()
