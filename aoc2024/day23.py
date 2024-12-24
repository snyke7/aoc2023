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


def find_connected_triples(nodes, graph):
    result = set()
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j] not in graph[nodes[i]]:
                continue
            overlap = graph[nodes[i]] & graph[nodes[j]]
            for el in overlap:
                result.add(tuple(sorted((nodes[i], nodes[j], el))))
    return result


def main():
    test_input = TEST_INPUT.splitlines()
    nodes, graph = build_graph(test_input)
    print(len(find_connected_triples(nodes, graph)))
    # find way to focus on t-nodes
    # download and test on real input
    # make sure the TEST_INPUT is correct, manually typed over


if __name__ == '__main__':
    main()
