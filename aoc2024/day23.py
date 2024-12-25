from typing import Dict, Set, Tuple, List


TEST_INPUT = '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''


def build_graph(connection_lines) -> Tuple[List[str], Dict[str, Set[str]]]:
    connections = {}
    nodes = set()
    for line in connection_lines:
        l, _, r = line.strip().partition('-')
        nodes.add(l)
        nodes.add(r)
        if l not in connections:
            connections[l] = set()
        connections[l].add(r)
        if r not in connections:
            connections[r] = set()
        connections[r].add(l)
    return list(nodes), connections


def find_connected_triples(all_nodes, graph, the_nodes=None):
    result = set()
    nodes = all_nodes
    if the_nodes is None:
        the_nodes = all_nodes
    for i in range(len(all_nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j] not in graph[nodes[i]]:
                continue
            overlap = graph[nodes[i]] & graph[nodes[j]]
            for el in overlap:
                to_add = tuple(sorted((nodes[i], nodes[j], el)))
                if not (set(to_add) & set(the_nodes)):
                    continue
                result.add(to_add)
    return result


def grow_party(base_party, graph):
    all_connected = graph[base_party[0]]
    for next_pc in base_party[1:]:
        all_connected = all_connected & graph[next_pc]
    return {
        tuple(sorted(set(base_party) | {el}))
        for el in all_connected
    }


def grow_parties(base_parties, graph):
    return {
        el
        for base_party in base_parties
        for el in grow_party(base_party, graph)
    }


def find_largest_party(nodes, graph):
    prev_parties = find_connected_triples(nodes, graph)
    next_parties = grow_parties(prev_parties, graph)
    while next_parties:
        prev_parties = next_parties
        next_parties = grow_parties(prev_parties, graph)
    return prev_parties


def main():
    test_input = TEST_INPUT.splitlines()
    with open('input/day23.txt') as f:
        test_input = f.readlines()
    nodes, graph = build_graph(test_input)
    t_nodes = [node for node in nodes if node.startswith('t')]
    print(len(find_connected_triples(nodes, graph, t_nodes)))
    largest_parties = find_largest_party(nodes, graph)
    print(largest_parties)
    the_largest = next(iter(largest_parties))
    print(','.join(the_largest))
    # find way to focus on t-nodes
    # download and test on real input
    # make sure the TEST_INPUT is correct, manually typed over


if __name__ == '__main__':
    main()
