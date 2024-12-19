from itertools import product

TEST_INPUT = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''


def parse_input(input_lines):
    towel_str, _, patterns_str = input_lines.partition('\n\n')
    towels = towel_str.strip().split(', ')
    patterns = [pat.strip() for pat in patterns_str.split('\n') if pat.strip()]
    return towels, patterns


COLORS = ['w', 'u', 'b', 'r', 'g']


def partial_pattern_maps(towels, depth):
    result = {}
    short_patterns = set()
    for el_tup in product(COLORS, repeat=depth):
        el = ''.join(el_tup)
        for pat in towels:
            if len(pat) < depth:
                short_patterns.add(pat)
            if pat.startswith(el):
                if el not in result:
                    result[el] = []
                # do we want more?
                result[el].append([pat])
    if depth <= 1:
        return {depth: result}
    shorter_pattern_maps = partial_pattern_maps(towels, depth - 1)
    for short_pat in short_patterns:
        rem_len = depth - len(short_pat)
        for postfix, rem_pats in shorter_pattern_maps[rem_len].items():
            if short_pat + postfix not in result:
                result[short_pat + postfix] = []
            result[short_pat + postfix].extend([
                [short_pat] + rem_pat for rem_pat in rem_pats
            ])
    shorter_pattern_maps[depth] = result
    return shorter_pattern_maps


def get_towel_combinations(pattern, pattern_maps, depth, towels):
    if not pattern:
        yield []
        return
    this_depth = min(len(pattern), depth)
    if this_depth == 0:
        print('Help')
        print(repr(pattern))
        print(depth)
    the_start = pattern[:this_depth]
    if the_start not in pattern_maps[this_depth]:
        return
    for towel_comb in pattern_maps[this_depth][the_start]:
        rem_pat = pattern
        for towel in towel_comb[:-1]:
            rem_pat = rem_pat[len(towel):]
        last_towel = towel_comb[-1]
        if not rem_pat.startswith(last_towel):
            continue
        for comb in get_towel_combinations(rem_pat[len(last_towel):], pattern_maps, depth, towels):
            yield towel_comb + comb


def can_make_pattern(pattern, pattern_map, depth, towels, scan_size):
    break_indices = find_guaranteed_breaks(pattern, towels, scan_size)
    if break_indices:
        with_max_split_lenghts = sorted([
            (idx, max(idx + scan_size, len(pattern) - idx - scan_size))
            for idx in break_indices
        ], key=lambda pr:-pr[1])
        break_idx = with_max_split_lenghts[0][0]
        # print(f'Breaking {pattern} at {break_idx}')
        for i in range(break_idx + 1, break_idx + scan_size):
            shortest = pattern[:i] if len(pattern[:i]) < len(pattern[i:]) else pattern[i:]
            longest = pattern[i:] if len(pattern[:i]) < len(pattern[i:]) else pattern[:i]
            if can_make_pattern(shortest, pattern_map, depth, towels, scan_size) and \
                can_make_pattern(longest, pattern_map, depth, towels, scan_size):
                return True
        return False
    for comb in get_towel_combinations(pattern, pattern_map, depth, towels):
        return True
    return False


def count_combinations(pattern, pattern_map, depth, towels, scan_size):
    break_indices = find_guaranteed_breaks(pattern, towels, scan_size)
    if break_indices:
        with_max_split_lenghts = sorted([
            (idx, max(idx + scan_size, len(pattern) - idx - scan_size))
            for idx in break_indices
        ], key=lambda pr:-pr[1])
        break_idx = with_max_split_lenghts[0][0]
        # print(f'Breaking {pattern} at {break_idx}')
        result = 0
        for i in range(break_idx + 1, break_idx + scan_size - 1):
            shortest = pattern[:i] if len(pattern[:i]) < len(pattern[i:]) else pattern[i:]
            longest = pattern[i:] if len(pattern[:i]) < len(pattern[i:]) else pattern[:i]
            short_combinations = count_combinations(shortest, pattern_map, depth, towels, scan_size)
            if short_combinations == 0:
                continue
            long_combinations = count_combinations(longest, pattern_map, depth, towels, scan_size)
            result += short_combinations * long_combinations
        return result
    return len(list(get_towel_combinations(pattern, pattern_map, depth, towels)))


def find_guaranteed_breaks(pattern, towels, scan_size):
    result = []
    for i in range(len(pattern) - scan_size + 1):
        scanning = pattern[i:i+scan_size]
        found = False
        for towel in towels:
            sub_idx = towel.find(scanning)
            if sub_idx == -1:
                continue
            if i - sub_idx < 0:
                continue
            if i - sub_idx + len(towel) > len(pattern):
                continue
            if pattern[i - sub_idx:i - sub_idx + len(towel)] == towel:
                found = True
                break
        if not found:
            result.append(i)
    return result


def main():
    test_input = TEST_INPUT
    # with open('input/day19.txt') as f:
    #     test_input = f.read()
    towels, patterns = parse_input(test_input)
    # print(towels)
    # print(patterns)
    depth = 5
    pattern_map = partial_pattern_maps(towels, depth)
    print('Computed map')
    # print(list(get_towel_combinations(patterns[0], pattern_map, depth, towels)))
    # patterns = ['bwgww']
    count = 0
    scan_size = 3
    # patterns = [patterns[2]]
    count_can_make = len([
        pat for pat in patterns
        if can_make_pattern(pat, pattern_map, depth, towels, scan_size)
    ])
    print(count_can_make)
    num_combs = [
        count_combinations(pat, pattern_map, depth, towels, scan_size)
        for pat in patterns
    ]
    print(num_combs)
    print(sum(num_combs))
    # print(len([pat for pat in patterns[:10] if can_make_pattern(pat, pattern_map, depth, towels)]))
    # print({
    #     pat: can_make_pattern(pat, pattern_map, depth, towels)
    #     for pat in patterns
    # })


if __name__ == '__main__':
    main()
