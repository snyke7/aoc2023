import re

TEST_INPUT = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
TEST_INPUT2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def part1(test_input):
    pats = re.findall('mul\([0-9]+,[0-9]+\)', test_input)
    mults = [tuple(map(int, pat[4:-1].split(','))) for pat in pats]
    return sum((a * b for a, b in mults))


def part2(test_input):
    start_enabled_parts = test_input.split('do()')
    enabled_parts = [part.split("don't()")[0] for part in start_enabled_parts]
    return sum((part1(part) for part in enabled_parts))


def main():
    test_input = TEST_INPUT2
    with open('input/day03.txt') as f:
        test_input = f.read()
    print(part1(test_input))
    print(part2(test_input))


if __name__ == '__main__':
    main()
