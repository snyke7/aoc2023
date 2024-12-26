import json


TEST_INPUT = ''''''


def sum_numbers(something):
    if isinstance(something, int):
        return something
    elif isinstance(something, str):
        return 0
    elif isinstance(something, list):
        return sum(map(sum_numbers, something))
    elif isinstance(something, dict):
        return sum(map(sum_numbers, something.keys())) + \
            sum(map(sum_numbers, something.values()))


def sum_numbers_no_red(something):
    if isinstance(something, int):
        return something
    elif isinstance(something, str):
        return 0
    elif isinstance(something, list):
        return sum(map(sum_numbers_no_red, something))
    elif isinstance(something, dict):
        if 'red' in something.values():
            return 0
        return sum(map(sum_numbers_no_red, something.keys())) + \
            sum(map(sum_numbers_no_red, something.values()))


def main():
    test_input = TEST_INPUT
    with open('input/day12.txt') as f:
        result = json.load(f)
    print(sum_numbers(result))
    print(sum_numbers_no_red(result))


if __name__ == '__main__':
    main()
