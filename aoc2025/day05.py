from typing import Tuple, List


TEST_INPUT = '''3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''


def parse_ingredients(ingredients_str):
    return list(map(int, ingredients_str.splitlines()))


def parse_ranges(ranges_str):
    return [
        (int(start), int(end))
        for start, _, end in (
            range_str.strip().partition('-')
            for range_str in ranges_str.splitlines()
        )
    ]


def is_fresh(ingredient, fresh_ranges):
    return any((
        ingredient in range(start, end + 1)
        for start, end in fresh_ranges
    ))


def parse_input(input_str):
    ranges_str, _ , ingredients = input_str.partition('\n\n')
    return parse_ranges(ranges_str), parse_ingredients(ingredients)


def count_fresh(ingredients, fresh_ranges):
    return sum((
        1
        for ingredient in ingredients
        if is_fresh(ingredient, fresh_ranges)
    ))


Range = Tuple[int, int]

def is_valid(r: Range):
    return r[0] <= r[1]


# another strategy would be to merge the ranges... :shrug:
def cut_out(existing: Range, to_add: Range) -> List[Range]:
    left_add: Range = (to_add[0], min(existing[0] - 1, to_add[1]))
    right_add: Range = (max(to_add[0], existing[1] + 1), to_add[1])
    return (
        ([left_add] if is_valid(left_add) else [])
        +
        ([right_add] if is_valid(right_add) else [])
    )


# recursion!
def non_overlapping_ranges(ranges: List[Range], to_add: Range) -> List[Range]:
    if len(ranges) == 0:
        return [to_add]
    else:
        return [
            el
            for to_add_el in cut_out(ranges[0], to_add)
            for el in non_overlapping_ranges(ranges[1:], to_add_el)
        ]


def build_non_overlapping_range_list(ranges: List[Range]) -> List[Range]:
    result = []
    for range_el in ranges:
        result.extend(non_overlapping_ranges(result, range_el))
    return result


def count_elements(ranges: List[Range]):
    return sum((
        end - start + 1
        for start, end in ranges
    ))


def main():
    ranges, ingredients = parse_input(TEST_INPUT)
    print(count_fresh(ingredients, ranges))
    print(count_elements(build_non_overlapping_range_list(ranges)))
    with open('input/day05.txt') as f:
        ranges, ingredients = parse_input(f.read())
    print(count_fresh(ingredients, ranges))
    print(count_elements(build_non_overlapping_range_list(ranges)))


if __name__ == '__main__':
    main()
