TEST_INPUT = '''987654321111111
811111111111119
234234234234278
818181911112111
'''


def find_max_joltage(bank, num_batteries):
    if num_batteries == 1:
        return max(bank)
    first_digit = max(bank[:-num_batteries + 1])
    first_digit_index = bank.index(first_digit)
    return first_digit * 10 ** (num_batteries - 1) + find_max_joltage(bank[first_digit_index+1:], num_batteries-1)


def read_banks(input_str):
    return [
        list(map(int, line))
        for line in input_str.splitlines()
    ]


def get_total_output_joltage(banks, num_batteries=2):
    return sum((find_max_joltage(bank, num_batteries) for bank in banks))


def main():
    banks = read_banks(TEST_INPUT)
    print(get_total_output_joltage(banks))
    print(get_total_output_joltage(banks, 12))
    with open('input/day03.txt') as f:
        banks = read_banks(f.read())
    print(get_total_output_joltage(banks))
    print(get_total_output_joltage(banks, 12))


if __name__ == '__main__':
    main()
