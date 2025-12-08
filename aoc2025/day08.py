from typing import Dict, List, Tuple

from utils import sub_coord


TEST_INPUT = '''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
'''


def parse_junctions(input_str):
    return [
        tuple(map(int, line.split(',')))
        for line in input_str.splitlines()
    ]


def compute_sq_distances(junctions):
    return sorted([
        ((i, j), sum(map(lambda c: c * c, sub_coord(left, right))))
        for i, left in enumerate(junctions)
        for j, right in enumerate(junctions[:i])
    ], key=lambda d: d[1])


def connect_junctions(junctions, num_connects):
    sq_dists = compute_sq_distances(junctions)
    junction_to_circuit_ids: Dict[int, int] = dict(enumerate(range(len(junctions))))
    circuit_ids_to_junctions: Dict[int, List[int]] = {i: [i] for i in range(len(junctions))}
    last_connection = (-1, -1)
    for (i, j), dist in sq_dists[:num_connects]:
        left_circuit = junction_to_circuit_ids[i]
        right_circuit = junction_to_circuit_ids[j]
        if left_circuit == right_circuit:
            continue  # what about the num_connects?
        add_to_left = circuit_ids_to_junctions[right_circuit]
        for right_circuit_el in add_to_left:
            junction_to_circuit_ids[right_circuit_el] = left_circuit
        circuit_ids_to_junctions[right_circuit] = []
        circuit_ids_to_junctions[left_circuit].extend(add_to_left)
        last_connection = (i, j)
        if len(circuit_ids_to_junctions[left_circuit]) == len(junctions):
            # fully connected, nothing left to do
            break
    return circuit_ids_to_junctions, last_connection


def compute_pt1(junctions, num_connects):
    circuits, last_conn = connect_junctions(junctions, num_connects)
    circuit_sizes = sorted(map(len, circuits.values()), reverse=True)
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def compute_pt2(junctions):
    circuits, (i, j) = connect_junctions(junctions, len(junctions) ** 2)
    return junctions[i][0] * junctions[j][0]


def main():
    junctions = parse_junctions(TEST_INPUT)
    print(compute_pt1(junctions, 10))
    print(compute_pt2(junctions))
    with open('input/day08.txt') as f:
        junctions = parse_junctions(f.read())
    print(compute_pt1(junctions, 1000))
    print(compute_pt2(junctions))


if __name__ == '__main__':
    main()
