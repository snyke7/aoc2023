from typing import TypeVar, Dict, List, Tuple


A = TypeVar('A')


def dijkstra(graph: Dict[A, List[Tuple[A, int]]], start: A) -> Dict[A, int]:
    result = {start: 0}
    new = [start]
    while new:
        node = new.pop(0)
        cost = result[node]
        for neigbor, dist in graph[node]:
            if neigbor not in result or result[neigbor] > cost + dist:
                result[neigbor] = cost + dist
                new.append(neigbor)
    return result


def step_to_dist_graph(graph: Dict[A, List[A]]) -> Dict[A, List[Tuple[A, int]]]:
    return {a: [(b, 1) for b in neighbors] for a, neighbors in graph.items()}


def dijkstra_steps(graph: Dict[A, List[A]], start: A) -> Dict[A, int]:
    return dijkstra(step_to_dist_graph(graph), start)


def file_read_lines(filename: str):
    with open(filename) as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def file_read(filename: str):
    with open(filename) as f:
        return f.read()


Coord2 = Tuple[int, int]
UP2 = (-1, 0)
DOWN2 = (1, 0)
LEFT2 = (0, -1)
RIGHT2 = (0, 1)


def add_coord(base: Tuple[int, ...], move: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(map(sum, zip(base, move)))


