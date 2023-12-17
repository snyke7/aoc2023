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


def dijkstra_steps(graph: Dict[A, List[A]], start: A) -> Dict[A, int]:
    return dijkstra({a: [(b, 1) for b in neighbors] for a, neighbors in graph.items()}, start)
