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


def main():
    test_input = TEST_INPUT2
    with open('input/day24.txt') as f:
        test_input = f.read()
    initial, gates = parse_input(test_input)
    result = simulate(initial, gates)
    z_keys = list(reversed(sorted((key for key in result.keys() if key.startswith('z')))))
    binary_num = ''.join((str(result[z_key]) for z_key in z_keys))
    print(int(binary_num, 2))


if __name__ == '__main__':
    main()
