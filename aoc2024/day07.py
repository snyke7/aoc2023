import itertools


TEST_INPUT = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''


def read_equation_component(line):
    result, _, raw_components = line.partition(':')
    return int(result), list(map(int, raw_components.strip().split(' ')))


def read_equation_components(lines):
    return [read_equation_component(line) for line in lines if line.strip()]


def get_operator_candidates_pt1(result, components):
    candidates = []
    for op_ids in itertools.product(range(2), repeat=len(components) - 1):
        the_result = components[0]
        for op_id, arg in zip(op_ids, components[1:]):
            if op_id == 0:
                the_result += arg
            else:  # op_id == 1
                the_result *= arg
        if the_result == result:
            candidates.append(op_ids)
    return candidates


def get_operator_candidates_pt2(result, components):
    candidates = []
    for op_ids in itertools.product(range(3), repeat=len(components) - 1):
        the_result = components[0]
        for op_id, arg in zip(op_ids, components[1:]):
            if op_id == 0:
                the_result += arg
            elif op_id == 1:
                the_result *= arg
            else:
                the_result = int(str(the_result) + str(arg))
        if the_result == result:
            candidates.append(op_ids)
    return candidates


def main():
    test_input = TEST_INPUT.splitlines()
    with open('input/day07.txt') as f:
        test_input = f.readlines()
    components = read_equation_components(test_input)
    # print(components)
    print(sum([result for result, comps in components if get_operator_candidates_pt1(result, comps) != []]))
    # again, terrible complexity, but it seems to suffice
    # we could have done something smarter by quitting early if the intermediate result was too big
    print(sum([result for result, comps in components if get_operator_candidates_pt2(result, comps) != []]))


if __name__ == '__main__':
    main()
