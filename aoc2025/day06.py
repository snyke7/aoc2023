from functools import reduce

TEST_INPUT = '''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
'''


def read_inputs(input_str):
    separated_inputs = [
        [el for el in line.split(' ') if el]
        for line in input_str.splitlines()
    ]
    return [list(map(int, nums)) for nums in separated_inputs[:-1]], separated_inputs[-1]


def get_op_and_initial(op_str):
    if op_str == '+':
        return (lambda x, y: x + y), 0
    elif op_str == '*':
        return (lambda x, y: x * y), 1
    else:
        raise ValueError(f"Unknown op {op_str}")


def compute_result(num_lists, ops):
    result = 0
    for i, op_str in enumerate(ops):
        the_op, initial = get_op_and_initial(op_str)
        result += reduce(the_op, [nums[i] for nums in num_lists], initial)
    return result


def read_inputs_pt2(input_str):
    as_rows = input_str.splitlines()
    transposed = [
        ''.join([
            as_rows[i][j]
            for i in range(len(as_rows))
        ]).strip()
        for j in range(len(as_rows[0]))
    ]
    result = []
    cur_prob = []
    for el in transposed:
        if el == '':
            result.append(cur_prob)
            cur_prob = []
        else:
            cur_prob.append(el)
    result.append(cur_prob)
    return result


def compute_result2(the_probs):
    result = 0
    for prob in the_probs:
        the_op, initial = get_op_and_initial(prob[0][-1])
        result += reduce(the_op, (
            int(operand)
            for operand in prob[1:]
        ), the_op(initial, int(prob[0][:-1])))
    return result


def main():
    num_lists, ops = read_inputs(TEST_INPUT)
    print(compute_result(num_lists, ops))
    the_probs = read_inputs_pt2(TEST_INPUT)
    print(compute_result2(the_probs))
    with open('input/day06.txt') as f:
        input_str = f.read()
    num_lists, ops = read_inputs(input_str)
    print(compute_result(num_lists, ops))
    the_probs = read_inputs_pt2(input_str)
    print(compute_result2(the_probs))


if __name__ == '__main__':
    main()
