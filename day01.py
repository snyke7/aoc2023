from itertools import chain


def get_calibration_value1(line: str):
    digits = [c for c in line if c.isdigit()]
    return int(digits[0] + digits[-1])


digit_strings = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}  # overlaps: twone eightree eightwo oneight threeight fiveight sevenine


def get_calibration_value2(line: str):
    min_idx = next(chain((i for i, c in enumerate(line) if c.isdigit()), [len(line)]))
    min_idx_str = None
    max_idx = next(chain((i for i, c in reversed(list(enumerate(line))) if c.isdigit()), [-1]))
    max_idx_str = None
    for digitstr in digit_strings.keys():
        idx = line.find(digitstr)
        if idx != -1 and idx < min_idx:
            min_idx = idx
            min_idx_str = digitstr

        idx = line.rfind(digitstr)
        if idx != -1 and idx > max_idx:
            max_idx = idx
            max_idx_str = digitstr
    if min_idx_str is not None:
        line = line.replace(min_idx_str, str(digit_strings[min_idx_str]), 1)
    if max_idx_str is not None:
        line = line.replace(max_idx_str, str(digit_strings[max_idx_str]))
    print(line)
    return get_calibration_value1(line)


def main():
    with open('input/day01_input.txt') as f:
        lines = f.readlines()
        result1 = sum((get_calibration_value1(line) for line in lines))
        result2 = sum((get_calibration_value2(line) for line in lines))
    print(result1)
    print(result2)
    test2 = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''
    print([get_calibration_value2(line) for line in test2.splitlines()])
    print(get_calibration_value2('pcg91vqrfpxxzzzoneightzt'))


if __name__ == '__main__':
    main()
