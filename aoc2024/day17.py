TEST_INPUT = '''Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
'''


TEST_INPUT2 = '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
'''


def read_machine(raw_input):
    register_str, _, program_str = raw_input.partition('\n\n')
    register = {
        line.partition(':')[0][-1]: int(line.partition(':')[2].strip())
        for line in register_str.splitlines()
    }
    program = list(map(int, program_str.partition(':')[2].strip().split(',')))
    register['pc'] = 0
    return register, program


def get_combo_operand(register, op):
    if op < 4:
        return op
    elif op == 4:
        return register['A']
    elif op == 5:
        return register['B']
    elif op == 6:
        return register['C']
    else:
        raise ValueError('Bad combo operand')


def adv(register, op):
    num = register['A']
    denom = 2 ** get_combo_operand(register, op)
    register['A'] = num // denom
    register['pc'] += 2


def bxl(register, op):
    register['B'] = register['B'] ^ op
    register['pc'] += 2


def bst(register, op):
    register['B'] = get_combo_operand(register, op) % 8
    register['pc'] += 2


def jnz(register, op):
    if register['A'] == 0:
        register['pc'] += 2
        return
    register['pc'] = op


def bxc(register, op):
    register['B'] = register['B'] ^ register['C']
    register['pc'] += 2


def out(register, op):
    result = get_combo_operand(register, op) % 8
    register['pc'] += 2
    return result


def bdv(register, op):
    num = register['A']
    denom = 2 ** get_combo_operand(register, op)
    register['B'] = num // denom
    register['pc'] += 2


def cdv(register, op):
    num = register['A']
    denom = 2 ** get_combo_operand(register, op)
    register['C'] = num // denom
    register['pc'] += 2


OPCODES = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def run_program_on(register, program):
    outputs = []
    while register['pc'] < len(program):
        opcode = program[register['pc']]
        operand = program[register['pc'] + 1]
        output = OPCODES[opcode](register, operand)
        if output is not None:
            outputs.append(output)
    return outputs


# works for test example, but we need to be smarter for actual input
def find_self_image(register, program, initial=0):
    a_value = initial
    while True:
        register['A'] = a_value
        register['pc'] = 0
        outputs = run_program_on(register, program)
        if (len(outputs) == len(program) and
                all((
            o == p
            for o, p in zip(outputs, program)
        ))):
            return a_value
        if outputs and outputs[0] != predict_output(a_value):
            print(a_value)
            break
        a_value += 1
        if a_value % 50000 == 0 and a_value != 0:
            print(a_value)
            print(outputs)
            print(program)


# obtained from manually analyzing program
def predict_output(a):
    return (
        (a % 8) ^ 1 ^ 5 ^ (a // (2 ** ((a % 8) ^ 1)))
    ) % 8


# obtained by rewriting predicted_output and simplifying
def solution_starts(desired_output):
    for low_bits in range(8):
        # output = lowbit ^ 4 ^ (a // 2 ** (lowbit ^ 1)) % 8
        bitshift = low_bits ^ 1
        shifted_bits = desired_output ^ low_bits ^ 4
        # these may disagree, below function fixes that
        yield low_bits, bitshift, shifted_bits


def solution_starts_as_bit_dicts(desired_output):
    for low_bits, bitshift, shifted_bits in solution_starts(desired_output):
        result = {}
        is_sane = True
        for i in range(3):
            result[i] = (low_bits // (2 ** i)) & 1
        for i in range(3):
            new_val = (shifted_bits // (2 ** i)) & 1
            if bitshift + i in result and result[bitshift + i] != new_val:
                is_sane = False
                break
            result[bitshift + i] = new_val
        if is_sane:
            yield result


def find_desired_input(desired_outputs, start_bit_dict):
    if len(desired_outputs) == 0:
        yield sum((v * 2 ** i for i, v in start_bit_dict.items()))
        return
    for bit_cand in solution_starts_as_bit_dicts(desired_outputs[0]):
        if any((start_bit_dict[k] != v for k, v in bit_cand.items() if k in start_bit_dict)):
            continue
        next_bit_dict = {**bit_cand, **start_bit_dict}
        for high_bits in find_desired_input(desired_outputs[1:], {i - 3: v for i, v in next_bit_dict.items() if i > 3}):
            yield high_bits * 2 ** 3 + sum((v * 2 ** i for i, v in bit_cand.items() if i < 3))


def find_desired_input_checked(desired_outputs, register, program):
    real_results = []
    for result in find_desired_input(desired_outputs, {}):
        register['A'] = result
        register['pc'] = 0
        # not entirely sure, but some returned possible inputs are bogus.
        # so we check them explicitly
        actual_outputs = run_program_on(register, program)
        if any((o != p for o, p in zip(actual_outputs, desired_outputs))):
            continue
        real_results.append(result)
    return real_results


def main():
    test_input = TEST_INPUT2
    with open('input/day17.txt') as f:
        test_input = f.read()
    register, program = read_machine(test_input)
    outputs = run_program_on(register, program)
    print(','.join(map(str, outputs)))
    results = find_desired_input_checked(program, register, program)
    print(min(results))


if __name__ == '__main__':
    main()
