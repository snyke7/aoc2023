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
                    result[el] = {}
                if pat not in result[el]:
                    result[el][pat] = []
                # do we want more?
                result[el][pat].append([pat])
    if depth <= 1:
        return {depth: result}
    shorter_pattern_maps = partial_pattern_maps(towels, depth - 1)
    for short_pat in short_patterns:
        rem_len = depth - len(short_pat)
        for postfix, rem_pat_dict in shorter_pattern_maps[rem_len].items():
            if short_pat + postfix not in result:
                result[short_pat + postfix] = {}
            for rem_pat_incl_tail, combs in rem_pat_dict.items():
                if short_pat + rem_pat_incl_tail not in result[short_pat + postfix]:
                    result[short_pat + postfix][short_pat + rem_pat_incl_tail] = []
                result[short_pat + postfix][short_pat + rem_pat_incl_tail].extend([
                    [short_pat] + rem_pat for rem_pat in combs
                ])
    shorter_pattern_maps[depth] = result
    return shorter_pattern_maps


def get_towel_combinations(pattern, pattern_maps, depth, towels):
    if not pattern:
        yield []
        return
    this_depth = min(len(pattern), depth)
    the_start = pattern[:this_depth]
    if the_start not in pattern_maps[this_depth]:
        return
    for full_pat, the_combs in pattern_maps[this_depth][the_start].items():
        if not pattern.startswith(full_pat):
            continue
        for comb_pat in the_combs:
            for comb in get_towel_combinations(pattern[len(full_pat):], pattern_maps, depth, towels):
                yield comb_pat + comb


def get_towel_combination_count(pattern, pattern_maps, depth, towels, rec_depth=0):
    if not pattern:
        return 1
    this_depth = min(len(pattern), depth)
    the_start = pattern[:this_depth]
    if the_start not in pattern_maps[this_depth]:
        return 0
    result = 0
    for full_pat, the_combs in pattern_maps[this_depth][the_start].items():
        if not pattern.startswith(full_pat):
            continue
        # if rec_depth <= 0:
        #     print(f'Investigating {the_start} as {full_pat}')
        result += len(the_combs) * get_towel_combination_count(pattern[len(full_pat):], pattern_maps, depth, towels, rec_depth)
    return result


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
        result = 0
        assert scan_size == 3
        # i = break_idx + 1
        # j = break_idx + 2
        # total = break_at1_not2 + break_at2_not1 + break_at1_and2
        # break_at1 = break_at1_not2 + break_at1_and2
        # break_at2 = break_at2_not1 + break_at1_and2
        # so we substract everything that breaks at both 1 and 2
        # break_at1 = comb_upto1 * comb_from1
        # break_at2 = comb_upto2 * comb_from2
        # break_at1_and2 = comb_upto1 * (0 or 1) * comb_from2
        upto_1 = pattern[:break_idx + 1]
        from_1 = pattern[break_idx + 1:]
        upto_2 = pattern[:break_idx + 2]
        from_2 = pattern[break_idx + 2:]
        if pattern[break_idx + 1] in towels:
            upto1_combs = count_combinations(upto_1, pattern_map, depth, towels, scan_size)
            from1_combs = count_combinations(from_1, pattern_map, depth, towels, scan_size)
            # take extra care
            upto2_combs = count_combinations(upto_2, pattern_map, depth, towels, scan_size)
            from2_combs = count_combinations(from_2, pattern_map, depth, towels, scan_size)
            return upto1_combs * from1_combs + upto2_combs * from2_combs - upto1_combs * from2_combs
        else:
            shortest_1, longest_1 = tuple(sorted([upto_1, from_1], key=lambda pr: len(pr)))
            short1_combs = count_combinations(shortest_1, pattern_map, depth, towels, scan_size)
            shortest_2, longest_2 = tuple(sorted([upto_2, from_2], key=lambda pr: len(pr)))
            short2_combs = count_combinations(shortest_2, pattern_map, depth, towels, scan_size)
            if short1_combs == 0:
                combs1 = 0
            else:
                combs1 = short1_combs * count_combinations(longest_1, pattern_map, depth, towels, scan_size)
            if short2_combs == 0:
                combs2 = 0
            else:
                combs2 = short2_combs * count_combinations(longest_2, pattern_map, depth, towels, scan_size)
            return combs1 + combs2
        # for i in range(break_idx + 1, break_idx + scan_size):
        #     print(f'into {pattern[:i]} and {pattern[i:]}')
        #     # the naive look counts stuff double here, if we can break both at
        #     # i, and at break_idx.
        #     # with a fixed scan_size of 3, the situation is simpler, tho
        #     shortest = pattern[:i] if len(pattern[:i]) < len(pattern[i:]) else pattern[i:]
        #     longest = pattern[i:] if len(pattern[:i]) < len(pattern[i:]) else pattern[:i]
        #     short_combinations = count_combinations(shortest, pattern_map, depth, towels, scan_size)
        #     if short_combinations == 0:
        #         continue
        #     long_combinations = count_combinations(longest, pattern_map, depth, towels, scan_size)
        #     result += short_combinations * long_combinations
        # return result
    return get_towel_combination_count(pattern, pattern_map, depth, towels)


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
    with open('input/day19.txt') as f:
        test_input = f.read()
    towels, patterns = parse_input(test_input)
    # print(towels)
    # print(patterns)
    depth = 5
    pattern_map = partial_pattern_maps(towels, depth)
    print('Computed map')
    # print(towels)
    # print(list(get_towel_combinations(patterns[3], pattern_map, depth, towels)))
    # patterns = ['bwgww']
    count = 0
    scan_size = 3
    # patterns = [patterns[2]]
    count_can_make = len([
        pat for pat in patterns
        if can_make_pattern(pat, pattern_map, depth, towels, scan_size)
    ])
    print(count_can_make)
    num_combs = 0
    for i, pat in enumerate(patterns):
        this_count = count_combinations(pat, pattern_map, depth, towels, scan_size)
        print(f'{i}: {this_count}')
        num_combs += this_count
    print(num_combs)
    # print(len([pat for pat in patterns[:10] if can_make_pattern(pat, pattern_map, depth, towels)]))
    # print({
    #     pat: can_make_pattern(pat, pattern_map, depth, towels)
    #     for pat in patterns
    # })


if __name__ == '__main__':
    main()
