def get_diff(seq):
    return [sn - sp for sn, sp in zip(seq[1:], seq[:-1])]


def predict_next(seq):
    if all((i == 0 for i in seq)):
        return 0
    next_diff = predict_next(get_diff(seq))
    return seq[-1] + next_diff


def predict_prev(seq):
    if all((i == 0 for i in seq)):
        return 0
    next_diff = predict_prev(get_diff(seq))
    return seq[0] - next_diff


def main():
    with open('input/day09_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''.splitlines()
    sequences = [
        list(map(int, line.strip().split(' ')))
        for line in input_lines
    ]
    print(sum((predict_next(seq) for seq in sequences)))
    print(sum((predict_prev(seq) for seq in sequences)))


if __name__ == '__main__':
    main()
