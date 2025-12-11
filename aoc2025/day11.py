from typing import TypeVar, Dict, List

from utils import dijkstra_steps


TEST_INPUT = '''aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
'''


TEST_INPUT_PT2 = '''svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
'''


A = str
Graph = Dict[A, List[A]]


def parse_as_graph(input_str) -> Graph:
    result = {
        line[:3]: line[5:].split(' ')
        for line in input_str.splitlines()
    }
    result['out'] = []
    return result


def count_paths_to(start: A, sources: Graph, sinks: Graph) -> Dict[A, int]:
    result = {start: 1}
    to_process = list(sinks[start])
    while to_process:
        dest = to_process.pop(0)  # pop first element (BFS!)
        # print(f'Processing: {dest}')
        # invariant: all elements of to_process have all necesarry info to compute #paths
        paths_to_dest = sum((result[src] for src in sources[dest]))
        result[dest] = paths_to_dest
        if dest not in sinks:
            continue
        for sink in sinks[dest]:
            # only add if all the sources of sink have been computed
            if all((src in result for src in sources[sink])):
                # print(f'Saw all of {sources[sink]} in {result}')
                to_process.append(sink)
    return result


def compute_sources(start: A, graph: Graph) -> Graph:
    result = {}
    reachable = set(dijkstra_steps(graph, start).keys())
    for src, sinks in graph.items():
        if src not in reachable:
            continue
        for sink in sinks:
            if sink not in result:
                result[sink] = []
            result[sink].append(src)
    return result


def solve_pt1(sinks):
    start = 'you'
    sources = compute_sources(start, sinks)
    num_paths = count_paths_to(start, sources, sinks)
    return num_paths['out']


def solve_pt2(sinks):
    start = 'svr'
    fft = 'fft'
    dac = 'dac'
    out = 'out'

    svr_sources = compute_sources(start, sinks)
    svr_paths = count_paths_to(start, svr_sources, sinks)

    fft_sources = compute_sources(fft, sinks)
    fft_paths = count_paths_to(fft, fft_sources, sinks)

    dac_sources = compute_sources(dac, sinks)
    dac_paths = count_paths_to(dac, dac_sources, sinks)

    # I dont think back flow is possible at all?
    if fft not in dac_paths:
        # svr -> fft -> dac -> out
        return svr_paths[fft] * fft_paths[dac] * dac_paths[out]
    else:
        assert(dac not in fft_paths)
        # svr -> dac -> fft -> out
        return svr_paths[dac] * dac_paths[fft] * fft_paths[out]


def main():
    sinks = parse_as_graph(TEST_INPUT)
    print(solve_pt1(sinks))
    sinks = parse_as_graph(TEST_INPUT_PT2)
    print(solve_pt2(sinks))
    with open('input/day11.txt') as f:
        sinks = parse_as_graph(f.read())
    print(solve_pt1(sinks))
    print(solve_pt2(sinks))


if __name__ == '__main__':
    main()
