TEST_INPUT = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''


def parse_pattern(raw_pat):
    return [
        list(line.strip())
        for line in raw_pat.split('\n')
        if line.strip()
    ]


def find_horizontal_reflection(pattern):
    for i in range(0, len(pattern) - 1):
        if all((
            pattern[i - j][n] == pattern[i + j + 1][n]
            for j in range(min(i + 1, len(pattern) - i - 1))
            for n in range(len(pattern[0]))
        )):
            return i
    return -1


def find_vertical_reflection(pattern):
    for i in range(0, len(pattern[0]) - 1):
        if all((
            pattern[n][i - j] == pattern[n][i + j + 1]
            for j in range(min(i + 1, len(pattern[0]) - i - 1))
            for n in range(len(pattern))
        )):
            return i
    return -1


def has_exactly_one_false(the_iter):
    false_count = 0
    try:
        while True:
            val = next(the_iter)
            if val is False:
                false_count += 1
                if false_count > 1:
                    return False
    except StopIteration:
        return false_count == 1


def find_horizontal_smudge_reflection(pattern):
    for i in range(0, len(pattern) - 1):
        if has_exactly_one_false((
            pattern[i - j][n] == pattern[i + j + 1][n]
            for j in range(min(i + 1, len(pattern) - i - 1))
            for n in range(len(pattern[0]))
        )):
            return i
    return -1


def find_vertical_smudge_reflection(pattern):
    for i in range(0, len(pattern[0]) - 1):
        if has_exactly_one_false((
            pattern[n][i - j] == pattern[n][i + j + 1]
            for j in range(min(i + 1, len(pattern[0]) - i - 1))
            for n in range(len(pattern))
        )):
            return i
    return -1


def find_reflection(pattern):
    vert_refl = find_vertical_reflection(pattern)
    if vert_refl != -1:
        return vert_refl + 1
    horiz_refl = find_horizontal_reflection(pattern)
    if horiz_refl != -1:
        return 100 * (horiz_refl + 1)
    return -1


def find_smudge_reflection(pattern):
    vert_refl = find_vertical_smudge_reflection(pattern)
    if vert_refl != -1:
        return vert_refl + 1
    horiz_refl = find_horizontal_smudge_reflection(pattern)
    if horiz_refl != -1:
        return 100 * (horiz_refl + 1)
    return -1


def main():
    with open('input/day13_input.txt') as f:
        raw_input = f.read()
    raw_input2 = TEST_INPUT
    patterns = [parse_pattern(raw_pat) for raw_pat in raw_input.split('\n\n')]
    summary = [find_reflection(pattern) for pattern in patterns]
    print(sum(summary))
    smudge_summary = [find_smudge_reflection(pattern) for pattern in patterns]
    print(sum(smudge_summary))


if __name__ == '__main__':
    main()
