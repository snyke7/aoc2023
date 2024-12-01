from typing import TypeVar, Dict, List, Tuple, Optional
from collections import defaultdict

from utils import step_to_dist_graph, dijkstra


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


def dijkstra_longest_heuristic(graph: Dict[A, List[Tuple[A, int]]], start: A) -> Dict[A, Tuple[List[A], int]]:
    result = {start: ([start], 0)}
    new_paths = [([start], 0)]
    time = 0
    while new_paths:
        new_path, this_length = new_paths.pop(0)
        prev = new_path[-1]
        for neighbor, dist in graph[prev]:
            if neighbor not in new_path:
                should_follow = (neighbor not in result or
                                 result[neighbor][1] < this_length + dist)
                if should_follow:
                    result[neighbor] = (new_path + [neighbor], this_length + dist)
                    new_paths.append((new_path + [neighbor], this_length + dist))
        time += 1
    return result


def can_reach_end(graph: Dict[A, List[Tuple[A, int]]], path: List[A], end: A) -> bool:
    if path[-1] == end:
        return True
    changed_graph = graph.copy()
    for el in path[:-1]:
        changed_graph[el] = []
    short_reach = dijkstra(changed_graph, path[-1])
    return end in short_reach


def dijkstra_longest(graph: Dict[A, List[Tuple[A, int]]], start: A, end: A) \
        -> Dict[A, Tuple[List[A], int]]:
    heuristic_result = dijkstra_longest_heuristic(graph, start)
    result = {}
    new_paths = [([start], 0)]
    while new_paths:
        new_path, this_length = new_paths.pop()
        # pops the lastest, making this DFS. DFS is crucial, the memory management for BFS otherwise makes it SLOW
        prev = new_path[-1]
        for neighbor, dist in graph[prev]:
            if neighbor not in new_path and can_reach_end(graph, new_path + [neighbor], end):
                if neighbor not in result or result[neighbor][1] < this_length + dist:
                    result[neighbor] = (new_path + [neighbor], this_length + dist)
                    if neighbor == end:
                        print(f'Found longer path: {result[neighbor][1]}')
                new_paths.append((new_path + [neighbor], this_length + dist))
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


def compress_graph(the_graph: Dict[A, List[A]], start: A) -> Dict[A, List[Tuple[A, int]]]:
    result: Dict[A, Dict[A, Tuple[A, int]]] = {}
    new_paths = [[start, n2] for n2 in the_graph[start]]
    while new_paths:
        new_path = new_paths.pop()
        dist = 1
        while len(the_graph[new_path[-1]]) == 2:
            new_path.append(next((neighbor for neighbor in the_graph[new_path[-1]] if neighbor not in new_path)))
            dist += 1
        if new_path[0] not in result:
            result[new_path[0]] = {}
        result[new_path[0]][new_path[1]] = (new_path[-1], dist)
        for n2 in the_graph[new_path[-1]]:
            if new_path[-1] not in result:
                result[new_path[-1]] = {}
            if n2 in result[new_path[-1]]:
                continue
            new_paths.append([new_path[-1], n2])
    return {
        node: [
            (dest, dist)
            for dest, dist in next_map.values()
        ]
        for node, next_map in result.items()
    }


def main():
    with open('input/day23_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    start = (0, 1)
    end = (len(input_lines) - 1, len(input_lines[-1].strip()) - 2)

    graph_pt1 = parse_graph(input_lines, uphill=False)
    compressed_graph = compress_graph(graph_pt1, start)
    long_path1 = dijkstra_longest_heuristic(step_to_dist_graph(graph_pt1), start)
    print(long_path1[end][1])
    print(len(graph_pt1), len(compressed_graph))
    long_path1 = dijkstra_longest_heuristic(compressed_graph, start)
    print(long_path1[end][1])
    print()
    #
    graph_pt2 = parse_graph(input_lines, uphill=True)
    compressed_graph = compress_graph(graph_pt2, start)
    print(len(graph_pt2), len(compressed_graph))
    long_path2 = dijkstra_longest_heuristic(compressed_graph, start)
    print(long_path2[end][1])  # > 5662
    long_path2 = dijkstra_longest(compressed_graph, start, end)
    print(long_path2[end][1])  # > 5662


if __name__ == '__main__':
    main()
