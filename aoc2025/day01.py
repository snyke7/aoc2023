TEST = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
'''


def parse_input(input_lines):
    return [
        (1 if line[0] == 'R' else -1) * int(line[1:])
        for line in input_lines.splitlines()
    ]


def count_zero_partial_sum(instructions):
    partial_sum = 50
    tally = 0
    for i in instructions:
        partial_sum += i
        partial_sum %= 100
        if partial_sum == 0:
            tally += 1
    return tally


def count_clicks_pt2(instructions):
    partial_sum = 50
    tally = 0
    for i in instructions:
        prev_val = partial_sum
        partial_sum += i
        partial_sum %= 100
        if i > 0:
            tally += (prev_val + i) // 100
        else:
            tally += (((-1 * prev_val) % 100) - i) // 100
    return tally


def main():
    instructions = parse_input(TEST)
    print(count_zero_partial_sum(instructions))
    print(count_clicks_pt2(instructions))
    with open('input/day01.txt') as f:
        instructions = parse_input(f.read())
    print(count_zero_partial_sum(instructions))
    print(count_clicks_pt2(instructions))


if __name__ == '__main__':
    main()