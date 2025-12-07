from collections import defaultdict
from math import isnan
from typing import List, Set, Dict, Tuple

from utils import Coord2, DOWN2, LEFT2, RIGHT2, add_coord


TEST_INPUT = '''.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''


def read_map_str(map_str):
    start = None
    splitters = []
    max_x = -1
    for i, line in enumerate(map_str.splitlines()):
        for j, el in enumerate(line.strip()):
            if el == 'S':
                start = i, j
            elif el == '^':
                splitters.append((i, j))
        max_x = i
    return start, set(splitters), max_x


def get_hit_splitters(start: Coord2, splitters: Set[Coord2], max_x: int) -> Set[Coord2]:
    cur_loc = start
    while cur_loc not in splitters and cur_loc[0] < max_x:
        cur_loc = add_coord(cur_loc, DOWN2)
    if cur_loc in splitters:
        return (
            {cur_loc}
            | get_hit_splitters(add_coord(cur_loc, LEFT2), splitters, max_x)
            | get_hit_splitters(add_coord(cur_loc, RIGHT2), splitters, max_x)
        )
    else:
        return set()


def get_hit_splitters_fast(start: Coord2, splitters: Set[Coord2], max_x: int) -> Set[Coord2]:
    result = set()
    processed_beams = {start}
    pending_beams = [start]
    while pending_beams:
        cur_beam = pending_beams.pop()
        while cur_beam not in splitters and cur_beam[0] < max_x:
            cur_beam = add_coord(cur_beam, DOWN2)
            processed_beams.add(cur_beam)
        if cur_beam in splitters:
            result.add(cur_beam)
            for new_beam in [add_coord(cur_beam, LEFT2), add_coord(cur_beam, RIGHT2)]:
                if new_beam in processed_beams:
                    continue
                processed_beams.add(new_beam)
                pending_beams.append(new_beam)
    return result


def beam_down(start: Coord2, splitters: Set[Coord2], max_x: int) -> Coord2:
    cur_beam = tuple(start)
    while cur_beam not in splitters and cur_beam[0] < max_x:
        cur_beam = add_coord(cur_beam, DOWN2)
    return cur_beam


Graph = Dict[Coord2, List[Coord2]]


def into_directed_acyclic_graph(start: Coord2, splitters: Set[Coord2], max_x: int) -> Tuple[Graph, Graph]:
    sources = {}
    sinks = defaultdict(lambda: [])
    pending_beams: List[Tuple[Coord2, Coord2]] = [(start, start)]
    # (origin, beam) list
    while pending_beams:
        origin, cur_beam = pending_beams.pop()
        dest = beam_down(cur_beam, splitters, max_x)
        sinks[origin].append(dest)
        if dest in sources:
            sources[dest].append(origin)
            continue
        sources[dest] = [origin]
        if dest not in splitters:
            continue
        for new_beam in [add_coord(dest, LEFT2), add_coord(dest, RIGHT2)]:
            pending_beams.append((dest, new_beam))
    return sources, dict(sinks)


def count_paths_to(start: Coord2, sources: Graph, sinks: Graph) -> Dict[Coord2, int]:
    result = {start: 1}
    to_process = list(sinks[start])
    while to_process:
        dest = to_process.pop(0)  # pop first element (BFS!)
        # invariant: all elements of to_process have all necesarry info to compute #paths
        paths_to_dest = sum((result[src] for src in sources[dest]))
        result[dest] = paths_to_dest
        if dest not in sinks:
            continue
        for sink in sinks[dest]:
            # only add if all the sources of sink have been computed
            if all((src in result for src in sources[sink])):
                to_process.append(sink)
    return result


def count_timelines(start: Coord2, sources: Graph, sinks: Graph) -> int:
    num_paths = count_paths_to(start, sources, sinks)
    return sum((
        num_paths[el]
        for el in sources
        if el not in sinks
    ))


def main():
    start, splitters, max_x = read_map_str(TEST_INPUT)
    print(len(get_hit_splitters(start, splitters, max_x)))
    print(len(get_hit_splitters_fast(start, splitters, max_x)))
    sources, sinks = into_directed_acyclic_graph(start, splitters, max_x)
    print(count_timelines(start, sources, sinks))
    with open('input/day07.txt') as f:
        start, splitters, max_x = read_map_str(f.read())
    print(len(get_hit_splitters_fast(start, splitters, max_x)))
    sources, sinks = into_directed_acyclic_graph(start, splitters, max_x)
    print(count_timelines(start, sources, sinks))


if __name__ == '__main__':
    main()
