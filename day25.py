from typing import List

from attr import define, Factory

from utils import dijkstra_steps_path


TEST = '''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''


def parse_connection(line):
    left, _, rights_raw = line.partition(': ')
    return left, rights_raw.split(' ')


@define
class Node:
    name: str
    connections: List['Node'] = Factory(lambda: [])

    def __repr__(self):
        return f'Node(name={self.name}, connections={[n.name for n in self.connections]})'

    def __hash__(self):
        return hash(self.name)


def connect(n1, n2):
    n1.connections.append(n2)
    n2.connections.append(n1)


def disconnect(n1, n2):
    n1.connections.remove(n2)
    n2.connections.remove(n1)


def build_graph(connections):
    nodes = {}
    for left, rights in connections:
        for n in [left] + rights:
            if n not in nodes:
                nodes[n] = Node(n)
        for right in rights:
            connect(nodes[left], nodes[right])
    return nodes


def all_distinct_subsets_of_size(superlist, the_length):
    if the_length == 0:
        return [set()]
    elif the_length == 1:
        return [{el} for el in superlist]
    result = []
    for i, el in enumerate(superlist[:-(the_length - 1)]):
        rem_sets = all_distinct_subsets_of_size(superlist[i+1:], the_length-1)
        result.extend([rem_set | {el} for rem_set in rem_sets])
    return result


def edge_iter(graph):
    to_visit = [next(iter(graph.values()))]
    visited_nodes = set(to_visit)
    visited_edges = set()
    while to_visit:
        node = to_visit.pop(0)
        for n in node.connections:
            if frozenset({node, n}) not in visited_edges:
                yield node, n
                visited_edges.add(frozenset({node, n}))
            if n not in visited_nodes:
                to_visit.append(n)
                visited_nodes.add(n)


def group_nodes_cut3(graph):
    the_nodes = list(graph.values())
    time = 0
    for n1, n2 in edge_iter(graph):
        # we try to make n2 unreachable from n1. we must first cut the n1 -- n2 edge
        disconnect(n1, n2)
        # now find the shortest path from n1 to n2
        paths = dijkstra_steps_path({n: n.connections for n in the_nodes}, n1)
        shortest_path = paths[n2][1]
        for m1, m2 in zip(shortest_path[:-1], shortest_path[1:]):
            disconnect(m1, m2)
            # again, find the shortest path from n1 to n2
            paths2 = dijkstra_steps_path({n: n.connections for n in the_nodes}, n1)
            shortest_path2 = paths2[n2][1]
            for k1, k2 in zip(shortest_path2[:-1], shortest_path2[1:]):
                disconnect(k1, k2)
                paths3 = dijkstra_steps_path({n: n.connections for n in the_nodes}, n1)
                if n2 not in paths3:
                    print(f'Should cut: {n1.name, n2.name} and {m1.name, m2.name} and {k1.name, k2.name}')
                    s1 = len(paths3)
                    s2 = len(the_nodes) - s1
                    print(s1, s2, s1 * s2)
                    connect(k1, k2)
                    connect(m1, m2)
                    connect(n1, n2)
                    return s1 * s2
                connect(k1, k2)
            connect(m1, m2)
        connect(n1, n2)
        time += 1


def main():
    with open('input/day25_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    connections = [parse_connection(line.strip()) for line in input_lines]
    graph = build_graph(connections)
    print(group_nodes_cut3(graph))
    # print([n.name for n in graph.values() if len(n.connections) == 3])
    # print({len(n.connections) for n in graph.values()})


if __name__ == '__main__':
    main()
