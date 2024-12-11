from typing import List, Dict

TEST_INPUT_1 = '125 17'
REAL_INPUT = '2 72 8949 0 981038 86311 246 7636740'


def count_descendants(source, steps):
    if steps <= 0:
        return 1
    if source == 0:
        return count_descendants(1, steps - 1)
    else:
        str_source = str(source)
        if len(str_source) % 2 == 0:
            left_source = int(str_source[:len(str_source) // 2])
            left_part = count_descendants(left_source, steps - 1)
            right_source = int(str_source[len(str_source) // 2:])
            right_part = count_descendants(right_source, steps - 1)
            result = left_part + right_part
            if steps > 40:
                print(source, steps, result)
            return result
        else:
            return count_descendants(source * 2024, steps - 1)


# quite clever puzzle, as a direct lru_cache does not work!

DESCENDANTS_CACHE = {}

def descendant_evolution(source, steps) -> List[int]:
    # returns a list of length at least steps + 1, with the desired answer at index steps
    if steps <= 0:
        return [1]
    if source in DESCENDANTS_CACHE and steps < len(DESCENDANTS_CACHE[source]):
        return DESCENDANTS_CACHE[source]
    if source == 0:
        DESCENDANTS_CACHE[source] = [1] + descendant_evolution(1, steps - 1)
        return DESCENDANTS_CACHE[source]
    else:
        str_source = str(source)
        if len(str_source) % 2 == 0:
            left_source = int(str_source[:len(str_source) // 2])
            left_part = descendant_evolution(left_source, steps - 1)
            right_source = int(str_source[len(str_source) // 2:])
            right_part = descendant_evolution(right_source, steps - 1)
            DESCENDANTS_CACHE[source] = [1] + [l + r for l, r in zip(left_part, right_part)]
            return DESCENDANTS_CACHE[source]
        else:
            DESCENDANTS_CACHE[source] = [1] + descendant_evolution(source * 2024, steps - 1)
            return DESCENDANTS_CACHE[source]


def count_all_descendants(source_list, steps):
    return sum((count_descendants(source, steps) for source in source_list))


def count_all_descendants_pt2(source_list, steps):
    return sum((descendant_evolution(source, steps)[steps] for source in source_list))


def main():
    test_input = REAL_INPUT
    source_list = list(map(int, test_input.split()))
    print(count_all_descendants(source_list, 25))
    print(count_all_descendants_pt2(source_list, 25))
    print(count_all_descendants_pt2(source_list, 75))
    # print(count_all_descendants(list(map(int, test_input.split())), 75))

# x(0, 0) = [0]
# x(0, 1) = [1]
# x(0, 2) = [2024]
# x(0, 3) = [20, 24]
# x(0, 4) = [2, 0, 2, 4]
# x(0, 5) = [4048, 1, 4048, 8096]
# x(0, 6) = [40, 48, 2024, 40, 48, 80, 96]
# x(0, 7) = [4, 0, 4, 8, 20, 24, 4, 0, 4, 8, 8, 0, 9, 6]
# x(0, 8) = ...
#
#
# l(a, b) = len(x(a, b))
# l(x, 0) = 1
# l(0, 0) = 1
# l(0, 1) = 1
# l(0, 2) = 1
# l(0, 3) = 2
# l(0, 4) = 4
# l(0, 5) = 4
# l(0, 5 + b) =


if __name__ == '__main__':
    main()
