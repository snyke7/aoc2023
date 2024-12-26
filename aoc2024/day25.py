TEST_INPUT = '''#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''


def parse_key(key_text):
    key_lines = key_text.splitlines()
    return [
        sum((
            1
            for j in range(7)
            if key_lines[7 - 1 - j][i] == '#'
        )) - 1
        for i in range(5)
    ]


def parse_lock(lock_text):
    lock_lines = lock_text.splitlines()
    return [
        sum((
            1
            for j in range(7)
            if lock_lines[j][i] == '#'
        )) - 1
        for i in range(5)
    ]


def read_input(input_text):
    entries = input_text.split('\n\n')
    keys = []
    locks = []
    for entry in entries:
        if entry.strip().startswith('#' * 5):
            keys.append(parse_key(entry.strip()))
        elif entry.strip().endswith('#' * 5):
            locks.append(parse_lock(entry.strip()))
        else:
            raise ValueError(f'Bad entry: {entry}')
    return keys, locks


def count_fitting_locks(keys, locks):
    count = 0
    for key in keys:
        for lock in locks:
            max_add = max(map(sum, zip(key, lock)))
            if max_add <= 5:
                count += 1
    return count


def main():
    test_input = TEST_INPUT
    with open('input/day25.txt') as f:
        test_input = f.read()
    keys, locks = read_input(test_input)
    print(count_fitting_locks(keys, locks))


if __name__ == '__main__':
    main()
