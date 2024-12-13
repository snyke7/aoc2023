TEST_INPUT = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''


def is_symbol(character):
    return not character.isdigit() and character != '.'


def find_engine_parts(input_array):
    parts = []
    connected_num_dict = {}
    for i, line in enumerate(input_array):
        j = 0
        line_parts = []
        while j < len(line):
            while j < len(line) and not line[j].isdigit():
                j += 1
            startnum = j
            while j < len(line) and line[j].isdigit():
                j += 1
            endnum = j
            if startnum == endnum:
                continue
            symbol_locs = []
            for n in range(i - 1, i + 1 + 1):
                for m in range(startnum - 1, endnum + 1):
                    if 0 <= n < len(input_array) and 0 <= m < len(line) and is_symbol(input_array[n][m]):
                        symbol_locs.append((n, m))
            if symbol_locs:
                the_num = int(''.join(line[startnum:endnum]))
                line_parts.append(the_num)
                for loc in symbol_locs:
                    if loc not in connected_num_dict:
                        connected_num_dict[loc] = []
                    connected_num_dict[loc].append(the_num)
        parts.extend(line_parts)
    return sum(parts), connected_num_dict


def find_gears(num_dict, input_array):
    result = 0
    for n, m in num_dict.keys():
        nums = num_dict[(n,m)]
        if input_array[n][m] != '*' or len(nums) != 2:
            continue
        ratio = nums[0] * nums[1]
        result += ratio
    return result


def main():
    with open('input/day03_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST_INPUT.splitlines()
    input_array = [list(line.strip()) for line in input_lines]
    part1, num_dict = find_engine_parts(input_array)
    print(part1)
    print(find_gears(num_dict, input_array))


if __name__ == '__main__':
    main()
