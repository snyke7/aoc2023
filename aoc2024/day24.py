from typing import Dict, Set

from attr import define


TEST_INPUT1 = '''x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
'''


TEST_INPUT2 = '''x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''


TEST_INPUT3 = '''x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 and y05 -> z05
'''


def parse_gate(gate_txt):
    return tuple(gate_txt.split(' '))


def parse_input(input_text):
    initial_txt, _, gates_txt = input_text.partition('\n\n')
    initial = {
        line.strip().partition(': ')[0]: int(line.strip().partition(': ')[2])
        for line in initial_txt.splitlines()
        if line.strip()
    }
    gates = {
        line.strip().partition(' -> ')[2]: parse_gate(line.strip().partition(' -> ')[0])
        for line in gates_txt.splitlines()
        if line.strip()
    }
    return initial, gates


OP_DICT = {
    'AND': lambda l, r: l & r,
    'OR': lambda l, r: l | r,
    'XOR': lambda l, r: l ^ r,
}


def simulate(initial, gates):
    to_resolve = set(gates.keys())
    result = initial.copy()
    while to_resolve:
        for channel in list(to_resolve):
            left, op, right = gates[channel]
            if left not in result or right not in result:
                continue
            result[channel] = OP_DICT[op](result[left], result[right])
            to_resolve.remove(channel)
    return result


@define
class Node:
    name: str


@define
class InputNode(Node):
    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

@define
class GateNode(Node):
    name: str
    left_node: Node
    op: str
    right_node: Node

    def __str__(self):
        return f'{self.name}:({str(self.left_node)} {self.op} {str(self.right_node)})'

    def __hash__(self):
        return hash(self.name)

    def get_operands(self) -> Set[Node]:
        return {self.left_node, self.right_node}


def as_tree(inputs, gates):
    node_map: Dict[str, Node] = {name: InputNode(name) for name in inputs}
    rem_nodes = set(gates.keys())
    while rem_nodes:
        for key in list(rem_nodes):
            left, op, right = gates[key]
            if left not in node_map or right not in node_map:
                continue
            node_map[key] = GateNode(key, node_map[left], op, node_map[right])
            rem_nodes.remove(key)
    return node_map


# half adder:
# i1  [  ]  i1 xor x2
# i2  [  ]  i1 and x2
#
# full adder:
# i1  [  ] i1 xor i2 xor i3
# i2  [  ] (i1 and i2) or (i2 and i3) or (i1 and i3)
# i3  [  ]

# (i1 and i2) or ((i1 xor i2) and i3)










# z02 = x02 xor y02 xor ((x1 and y1) or (y1 and (x0 and y0)) or (x1 and (x0 and y0)))

# x01 = 1
# y01 = 1
#
# boolean equivalence checking!
# A <-> B iff (A /\ B) \/ (~A /\ ~B) is true
# iff ~((A /\ B) \/ (~A /\ ~B)) is unsat
# check if boolean formula is sat
# to DNF
# A \/ B \/ C \/ D
# where A = E /\ F /\ G /\ H /\ ..
# proceed and cancel


def make_full_adder(prefix: str, i1: Node, i2: Node, i3: Node):
    o1_pt1 = GateNode(prefix + '1_1', i1, 'XOR', i2)
    output = GateNode(prefix + '1', o1_pt1, 'XOR', i3)
    o2_pt1 = GateNode(prefix + '2_1', i1, 'AND', i2)
    o2_pt2 = GateNode(prefix + '2_3', o1_pt1, 'AND', i3)
    carry = GateNode(prefix + '2_4', o2_pt1, 'OR', o2_pt2)
    return output, carry, [o1_pt1, o2_pt1, o2_pt2]
# 5 nodes per output bit
# last one doesnt need one
# first one only needs 2
# num_gates(bit) = 2 + (bit - 2) * 5
# = 2 + 44 * 5 = 222


def make_adder(num_bits):
    left_inputs = [InputNode(f'x{i:02}') for i in range(num_bits)]
    right_inputs = [InputNode(f'y{i:02}') for i in range(num_bits)]
    all_gates: Set[Node] = set(left_inputs) | set(right_inputs)
    all_gates.add(GateNode('z00', left_inputs[0], 'XOR', right_inputs[0]))
    carry = GateNode('c00', left_inputs[0], 'AND', right_inputs[0])
    all_gates.add(carry)
    for i in range(1, num_bits):
        output, carry, intermediate = make_full_adder(f'o{i:02}', left_inputs[i], right_inputs[i], carry)
        output.name = f'z{i:02}'
        all_gates.add(output)
        all_gates.add(carry)
        all_gates.update(intermediate)
    return {gate.name: gate for gate in all_gates}


def is_valid_first_bit_adder(first_gate):
    if not isinstance(first_gate, GateNode):
        return False
    if first_gate.op != 'XOR':
        return False
    return {op.name for op in first_gate.get_operands()} == {'x00', 'y00'}


def decompose_second_gate(second_gate):
    these_ops, carry = (
        second_gate.left_node, second_gate.right_node) \
        if second_gate.left_node.op == 'XOR' else (
        second_gate.right_node, second_gate.left_node)
    if these_ops.op != 'XOR':
        raise ValueError('Bad these ops')
    if carry.op != 'AND':
        raise ValueError('Bad carry')
    return these_ops, carry


def decompose_adder_gate(adder_gate, prev_prev_carry, prev_ops, index):
    if not isinstance(adder_gate, GateNode):
        raise ValueError('adder_gate was an input node')
    if not isinstance(adder_gate.left_node, GateNode):
        raise ValueError('left_node of adder was an input node')
    if not isinstance(adder_gate.right_node, GateNode):
        raise ValueError('left_node of adder was an input node')
    if adder_gate.op != 'XOR':
        raise ValueError(f'adder_gate was not a XOR but a {adder_gate.op}')
    these_ops, carry = (
        adder_gate.left_node, adder_gate.right_node) \
        if adder_gate.left_node.op == 'XOR' else (
        adder_gate.right_node, adder_gate.left_node)
    supposed_these_op_operands = {f'{i}{index:02}' for i in {'x', 'y'}}
    actual_these_op_operands = {op.name for op in these_ops.get_operands()}
    if these_ops.op != 'XOR':
        raise ValueError(f'Bad these ops: expected a XOR of {supposed_these_op_operands} but got a {these_ops.op} of {actual_these_op_operands}')
    if actual_these_op_operands != supposed_these_op_operands:
        raise ValueError(f'Bad these ops: expected a XOR of {supposed_these_op_operands} but got {actual_these_op_operands}')
    if carry.op != 'OR':
        raise ValueError('Bad carry')
    prev_carry, prev_ops_and = (
        carry.left_node, carry.right_node
    ) if carry.left_node.get_operands() == {prev_prev_carry, prev_ops} else (
        carry.right_node, carry.left_node
    )
    if prev_carry.op != 'AND':
        raise ValueError('Bad prev carry')
    if prev_ops_and.op != 'AND':
        raise ValueError('Bad prev ops')
    if prev_ops_and.get_operands() != prev_ops.get_operands():
        raise ValueError(f'Bad prev ops operands. {prev_ops_and.get_operands()} vs {prev_ops.get_operands()}')
    if prev_carry.get_operands() != {prev_prev_carry, prev_ops}:
        raise ValueError('Bad prev carry operands')
    return these_ops, carry


def find_bad_adder_gates(adder_gates):
    first_gate = adder_gates[0]
    if not is_valid_first_bit_adder(first_gate):
        return first_gate
    try:
        second_gate_ops, first_carry = decompose_second_gate(adder_gates[1])
    except ValueError:
        return adder_gates[1]
    prev_ops, prev_prev_carry = second_gate_ops, first_carry
    for i, gate in enumerate(adder_gates[2:-1]):
        index = i + 2
        try:
            prev_ops, prev_prev_carry = decompose_adder_gate(gate, prev_prev_carry, prev_ops, index)
        except ValueError as e:
            print(e)
            return gate


def do_swap(gates, swapl, swapr):
    l = gates[swapl]
    r = gates[swapr]
    print(f'Swapping {l} and {r}')
    for gatename, gate in gates.items():
        if not isinstance(gate, GateNode):
            continue
        if gate.left_node.name == swapl:
            gate.left_node = r
        elif gate.left_node.name == swapr:
            gate.left_node = l
        if gate.right_node.name == swapl:
            gate.right_node = r
        elif gate.right_node.name == swapr:
            gate.right_node = l
    gates[swapl] = r
    r.name = swapl
    gates[swapr] = l
    l.name = swapr


def main():
    test_input = TEST_INPUT2
    with open('input/day24.txt') as f:
        test_input = f.read()
    initial, gates = parse_input(test_input)
    print(len(gates))
    result = simulate(initial, gates)
    z_keys = list(reversed(sorted((key for key in result.keys() if key.startswith('z')))))
    print(len(z_keys))
    binary_num = ''.join((str(result[z_key]) for z_key in z_keys))
    print(int(binary_num, 2))
    node_tree = as_tree(initial.keys(), gates)
    to_check = 4
    for i in range(to_check):
        gate_name = f'z0{i}'
        print(f'{gate_name}: {node_tree[gate_name]}')
    adder_tree = make_adder(to_check)
    for i in range(to_check):
        gate_name = f'z0{i}'
        print(f'{gate_name}: {adder_tree[gate_name]}')
    print(find_bad_adder_gates([node_tree[f'z{i:02}'] for i in range(len(z_keys))]))
    swap1 = 'qwf', 'cnk'
    do_swap(node_tree, swap1[0], swap1[1])
    print(find_bad_adder_gates([node_tree[f'z{i:02}'] for i in range(len(z_keys))]))
    swap2 = 'vhm', 'z14'
    do_swap(node_tree, swap2[0], swap2[1])
    print(find_bad_adder_gates([node_tree[f'z{i:02}'] for i in range(len(z_keys))]))
    swap3 = 'mps', 'z27'
    do_swap(node_tree, swap3[0], swap3[1])
    print(find_bad_adder_gates([node_tree[f'z{i:02}'] for i in range(len(z_keys))]))
    swap4 = 'msq', 'z39'
    do_swap(node_tree, swap4[0], swap4[1])
    print(find_bad_adder_gates([node_tree[f'z{i:02}'] for i in range(len(z_keys))]))
    all_swapped = list(sorted(set(swap1) | set(swap2) | set (swap3) | set(swap4)))
    print(','.join(all_swapped))

if __name__ == '__main__':
    main()
