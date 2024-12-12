from typing import List, Tuple, Dict

from utils import DIRECTIONS2, add_coord


TEST_INPUT1 = '''AAAA
BBCD
BBCC
EEEC'''

TEST_INPUT2 = '''OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
'''

TEST_INPUT3 = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''

TEST_INPUT4 = '''AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
'''

TEST_INPUT5 = '''EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
'''


def grow_group(start, input_lines):
    group = [start]
    to_visit = [start]
    el = input_lines[start[0]][start[1]]
    while to_visit:
        visiting = to_visit.pop()
        for direction in DIRECTIONS2:
            ni, nj = add_coord(visiting, direction)
            if not 0 <= ni < len(input_lines):
                continue
            if not 0 <= nj < len(input_lines[ni]):
                continue
            neighbor_el = input_lines[ni][nj]
            if neighbor_el != el:
                continue
            if (ni, nj) in group:
                continue
            group.append((ni, nj))
            to_visit.append((ni, nj))
    return group


def make_group_map(input_lines):
    groups: List[List[Tuple[int, int]]] = []
    group_index_map: Dict[Tuple[int, int], int] = {}
    for i, line in enumerate(input_lines):
        for j, el in enumerate(line):
            if (i, j) in group_index_map:
                continue
            new_idx = len(groups)
            groups.append(grow_group((i, j), input_lines))
            for group_coord in groups[new_idx]:
                group_index_map[group_coord] = new_idx
    return group_index_map, groups


def count_perimeter(group):
    result = 0
    for coord in group:
        for direction in DIRECTIONS2:
            if add_coord(coord, direction) not in group:
                result += 1
    return result


def calc_fence_cost_pt1(group):
    return len(group) * count_perimeter(group)


def count_sides(group):
    result = 0
    seen_borders: Dict[Tuple[int, ...], List[int]] = {}
    for coord in group:
        for di, direction in enumerate(DIRECTIONS2):
            border = add_coord(coord, direction)
            if border in group:
                continue
            if border in seen_borders:
                if direction in seen_borders[border]:
                    continue
            else:
                seen_borders[border] = []
            seen_borders[border].append(direction)
            # have not seen this side before
            # wlog, assume direction is up
            left = DIRECTIONS2[(di + 1) % 4]
            right = DIRECTIONS2[(di - 1) % 4]
            down = DIRECTIONS2[(di + 2) % 4]
            # now extend in L,R direction as far as possible
            for ext_dir in {left, right}:
                ext = border
                while True:
                    ext = add_coord(ext, ext_dir)
                    if ext in group:
                        break
                    if add_coord(ext, down) not in group:
                        break
                    if ext not in seen_borders:
                        seen_borders[ext] = []
                    seen_borders[ext].append(direction)
            result += 1
    return result


def calc_fence_cost_pt2(group):
    return len(group) * count_sides(group)

def main():
    test_input = TEST_INPUT1.splitlines()
    with open('input/day12.txt') as f:
        test_input = f.readlines()
    stripped_input = [line.strip() for line in test_input if line.strip()]
    group_idx_map, groups = make_group_map(stripped_input)
    # print(groups[0])
    # print(count_sides(groups[0]))
    # print([count_sides(group) for group in groups])
    print(sum([calc_fence_cost_pt1(group) for group in groups]))
    # print([stripped_input[group[0][0]][group[0][1]] for group in groups])
    print(sum([calc_fence_cost_pt2(group) for group in groups]))


if __name__ == '__main__':
    main()
