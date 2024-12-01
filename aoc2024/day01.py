import re

TEST_INPUT = '''3   4
4   3
2   5
1   3
3   9
3   3'''


def part1(input_lines):
    zipped_list = [list(map(int, re.split(' +', line.strip()))) for line in input_lines]
    list1 = sorted([el[0] for el in zipped_list])
    list2 = sorted([el[1] for el in zipped_list])
    dists = [abs(el1 - el2) for el1, el2 in zip(list1, list2)]
    return sum(dists)


def part2(input_lines):
    zipped_list = [list(map(int, re.split(' +', line.strip()))) for line in input_lines]
    list1 = sorted([el[0] for el in zipped_list])
    list2 = sorted([el[1] for el in zipped_list])
    sim_score = [el * list2.count(el) for el in list1]
    return sum(sim_score)


def main():
    # the_input = TEST_INPUT.splitlines()
    with open('input/day01.txt') as f:
        the_input = f.readlines()
    print(part1(the_input))
    print(part2(the_input))
    pass


if __name__ == '__main__':
    main()