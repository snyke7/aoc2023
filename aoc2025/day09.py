from functools import reduce
from typing import List, Tuple

from utils import sub_coord, add_coord


TEST_INPUT = '''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
'''


def parse_tiles(input_str):
    return [
        tuple(map(int, line.split(',')))
        for line in input_str.splitlines()
    ]


def compute_squares(tiles):
    return sorted([
        ((i, j), reduce((lambda x, y: x * y), map(lambda d: abs(d) + 1, (sub_coord(left, right))), 1))
        for i, left in enumerate(tiles)
        for j, right in enumerate(tiles[:i])
    ], key=lambda d: d[1], reverse=True)

def sort_line(lb: int, ub: int) -> Tuple[int, int]:
    return tuple(sorted((lb, ub)))


def get_lines(tiles: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int, int, bool]], List[Tuple[int, int, int, bool]]]:
    vert_lines = []
    horiz_lines = []
    closest_x_idx, closest_x = min(enumerate(tiles), key=lambda pr: (pr[1][0], pr[0]))
    if tiles[closest_x_idx + 1][1] == tiles[closest_x_idx][1]:
        closest_x_idx = closest_x_idx - 1
    vert_lines.append((closest_x[0], *sort_line(tiles[closest_x_idx][1], tiles[closest_x_idx + 1][1]), True))
    left_or_above_is_empty = True
    for prev, start, end in zip(
        tiles[closest_x_idx:] + tiles[:closest_x_idx - 1],
        tiles[closest_x_idx + 1:] + tiles[:closest_x_idx],
        tiles[closest_x_idx + 2:] + tiles[:closest_x_idx + 1]
    ):
        if start[0] == end[0]:
            # prev, start, end = (2,3), (7,3), (7,1), true   gives false
            # prev, start, end = (2,5), (9,5), (9,7), false  gives true
            left_or_above_is_empty ^= (prev[0] > start[0]) ^ (start[1] < end[1])
            vert_lines.append((start[0], *sort_line(start[1], end[1]), left_or_above_is_empty))
        elif start[1] == end[1]:
            # prev, start, end = (2,5), (2,3), (7,3), true   gives true
            # prev, start, end = (2,3), (2,5), (9,5), true   gives false
            left_or_above_is_empty ^= (prev[1] > start[1]) ^ (start[0] < end[0])
            horiz_lines.append((start[1], *sort_line(start[0], end[0]), left_or_above_is_empty))
        else:
            raise ValueError(start, end)
    # lexicographic sort is what we want here
    return sorted(vert_lines), sorted(horiz_lines)


def is_line_tiled(lb: int, ub: int, height: int, lines: List[Tuple[int, int, int, bool]]):
    log = False
    def mprint(*args):
        if log:
            print(*args)

    prev_pos = lb
    is_tiled = False
    last_tiled = is_tiled
    first_hit = False
    # print(lb, ub, height)
    # corners must be hit consecutively!
    prev_first_corner = False
    # relevant_lines = list(filter(lambda l: l[1] <= height <= l[2], lines))
    # mprint(relevant_lines)
    for line in filter(lambda l: l[1] <= height <= l[2], lines):
        mprint(line, prev_pos, is_tiled, first_hit, prev_first_corner)
        if line[0] < lb:
            if not first_hit:
                if line[1] < height < line[2]:
                    mprint('not yet hit')
                    last_tiled = line[3]
                elif not prev_first_corner:
                    mprint('start on edge')
                    prev_first_corner = True
                    last_tiled = True
                else:
                    prev_first_corner = False
                    last_tiled = line[3]
            continue
        if line[0] > ub:
            break
        if not first_hit:
            if line[0] - prev_pos > 0 and line[3] and not prev_first_corner:
                return False
            first_hit = True
            prev_pos = line[0]
        if line[1] < height < line[2]:
            is_tiled = not line[3]
        elif not prev_first_corner:
            mprint('next on edge')
            prev_first_corner = True
            is_tiled = not line[3]
        else:
            mprint('second corner')
            prev_first_corner = False
            is_tiled = True
        # lb <= line[0] <= ub and line[1] <= height <= line[2]. intersection
        if line[0] - prev_pos > 1 and not is_tiled:
            # then there was an untiled gap between previous pos and this line
            return False
        prev_pos = line[0]
        last_tiled = line[3] or prev_first_corner

    if ub - prev_pos > 0 and not last_tiled:
        mprint('hit')
        # then there was an untiled gap between previous pos and this line, when extended
        return False
    else:
        return True


'''

   #
   X
   X
#XX#
#XXXXXX#
  #XXXX#
  ##
   X
   X
#XX#XXX#



   #XXXX#
   XXXXXX
   XXXXXX
#XX#XXXXX
#XXXXXX#X
  #XXXX#X
  ##XXXXX
   XXXXXX
   XXXXXX
#XX#XXXXX
#XXXXXXX#


#     #
      X
      X
   #XX#
   #XXXXXX#
     #XXXX#
     ##
      X
      X
   #XX#XXX#
#         #   
'''


def run_tests():
    tiles = parse_tiles(TEST_INPUT)
    vert_lines, horiz_lines = get_lines(tiles)
    # print(vert_lines)
    assert(not is_line_tiled(7, 11, 0, vert_lines))

    assert(is_line_tiled(8, 11, 1, vert_lines))
    assert(is_line_tiled(7, 11, 1, vert_lines))
    assert(not is_line_tiled(6, 11, 1, vert_lines))
    assert(not is_line_tiled(7, 12, 1, vert_lines))

    assert(is_line_tiled(7, 11, 2, vert_lines))
    assert(not is_line_tiled(6, 11, 2, vert_lines))
    assert(not is_line_tiled(7, 12, 2, vert_lines))

    assert(is_line_tiled(2, 11, 3, vert_lines))
    assert(not is_line_tiled(1, 11, 3, vert_lines))
    assert(not is_line_tiled(2, 12, 3, vert_lines))

    assert(is_line_tiled(2, 11, 4, vert_lines))
    # does not work because it does not hit any vert_line!
    assert(is_line_tiled(4, 9, 4, vert_lines))
    assert(is_line_tiled(4, 11, 4, vert_lines))
    assert(is_line_tiled(2, 9, 4, vert_lines))
    assert(not is_line_tiled(1, 11, 4, vert_lines))
    assert(not is_line_tiled(2, 12, 4, vert_lines))

    assert(is_line_tiled(2, 11, 5, vert_lines))
    assert(not is_line_tiled(1, 11, 5, vert_lines))
    assert(not is_line_tiled(2, 12, 5, vert_lines))

    assert(is_line_tiled(9, 11, 6, vert_lines))
    assert(not is_line_tiled(8, 11, 6, vert_lines))
    assert(not is_line_tiled(9, 12, 6, vert_lines))

    assert(is_line_tiled(9, 11, 7, vert_lines))
    assert(not is_line_tiled(8, 11, 7, vert_lines))
    assert(not is_line_tiled(9, 12, 7, vert_lines))

    assert(not is_line_tiled(9, 11, 8, vert_lines))

    assert(not is_line_tiled(3, 5, 1, horiz_lines))

    for i in range(2, 7):
        assert(is_line_tiled(3, 5, i, horiz_lines))
        assert(not is_line_tiled(2, 5, i, horiz_lines))
        assert(not is_line_tiled(3, 6, i, horiz_lines))

    for i in range(7, 9):
        assert(is_line_tiled(1, 5, i, horiz_lines))
        assert(is_line_tiled(1, 4, i, horiz_lines))
        assert(is_line_tiled(1, 3, i, horiz_lines))
        assert(not is_line_tiled(1, 6, i, horiz_lines))
        assert(not is_line_tiled(0, 5, i, horiz_lines))

    for i in range(9, 12):
        assert(is_line_tiled(1, 7, i, horiz_lines))
        assert(not is_line_tiled(0, 7, i, horiz_lines))
        assert(not is_line_tiled(1, 8, i, horiz_lines))

    assert(not is_line_tiled(1, 7, 12, horiz_lines))

    assert(is_square_tiled((7, 3), (11, 1), horiz_lines, vert_lines))
    assert(not is_square_tiled((6, 3), (11, 1), horiz_lines, vert_lines))
    assert(not is_square_tiled((7, 3), (11, 0), horiz_lines, vert_lines))
    assert(not is_square_tiled((7, 3), (11, 0), horiz_lines, vert_lines))

    assert(is_square_tiled((9, 7), (9, 5), horiz_lines, vert_lines))

    assert(is_square_tiled((9, 5), (2, 3), horiz_lines, vert_lines))

    assert(is_line_tiled(1, 3, 9, horiz_lines))
    assert(is_line_tiled(2, 5, 11, horiz_lines))
    assert(is_line_tiled(2, 2, 2, horiz_lines))
    assert(is_line_tiled(5, 7, 9, horiz_lines))
    assert(is_line_tiled(6, 7, 9, horiz_lines))
    assert(is_line_tiled(6, 6, 9, horiz_lines))


def is_square_tiled(corner1, corner2, horiz_lines, vert_lines):
    log = False
    def mprint(the_str):
        if log:
            print(the_str)

    min_corner = tuple(map(min, zip(corner1, corner2)))
    max_corner = tuple(map(max, zip(corner1, corner2)))
    # optimization: do edges first
    if not is_line_tiled(min_corner[1], max_corner[1], min_corner[0], horiz_lines):
        mprint(f'y: {min_corner[1]}, {max_corner[1]}, {min_corner[0]}')
        return False
    if not is_line_tiled(min_corner[1], max_corner[1], max_corner[0], horiz_lines):
        mprint(f'y: {min_corner[1]}, {max_corner[1]}, {max_corner[0]}')
        return False
    if not is_line_tiled(min_corner[0], max_corner[0], min_corner[1], vert_lines):
        mprint(f'x: {min_corner[0]}, {max_corner[0]}, {min_corner[1]}')
        return False
    if not is_line_tiled(min_corner[0], max_corner[0], max_corner[1], vert_lines):
        mprint(f'x: {min_corner[0]}, {max_corner[0]}, {min_corner[1]}')
        return False

    horiz_tiled = True
    for i in range(min_corner[0], max_corner[0] + 1):
        if not is_line_tiled(min_corner[1], max_corner[1], i, horiz_lines):
            mprint(f'y: {min_corner[1]}, {max_corner[1]}, {i}')
            horiz_tiled = False
            break
    vert_tiled = True
    for j in range(min_corner[1], max_corner[1] + 1):
        if not is_line_tiled(min_corner[0], max_corner[0], j, vert_lines):
            mprint(f'x: {min_corner[0]}, {max_corner[0]}, {j}')
            vert_tiled = False
            break
    if horiz_tiled != vert_tiled:
        mprint(f'Investigate these corners: {corner1, corner2} with area: {abs((corner2[1] - corner1[1]) * (corner2[0] - corner1[0]))}')
        raise AssertionError
    return horiz_tiled


def solve_pt2(tiles):
    squares = compute_squares(tiles)
    vert_lines, horiz_lines = get_lines(tiles)
    result = None
    for idx, ((i, j), area) in enumerate(squares):
        if idx % 100 == 99:
            print(idx + 1)
        if is_square_tiled(tiles[i], tiles[j], horiz_lines, vert_lines):
            if result is None:
                print( (i, j), area, tiles[i], tiles[j])
                result = area
    return result
    raise ValueError("No squares")


def main():
    run_tests()
    run_tests_hole()
    tiles = parse_tiles(TEST_INPUT)
    print(compute_squares(tiles)[0][1])
    print(solve_pt2(tiles))
    with open('input/day09.txt') as f:
        tiles = parse_tiles(f.read())
    result = compute_squares(tiles)
    print(result[:10])
    print(result[0][1])
    print(solve_pt2(tiles))

    # 537411615 is too low


'''

#XXXXXXXXXXXXXXXXXXXXXXXXX#
XXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXX#XXXXXXXX#XXXXXX
XXXXXXXXXXXX        XXXXXXX
XXXXXXXXXXXX#XXXXXXX#XXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXX
#X#XXXXXXXXX#XXX#XXXXXXXXXX
  XXXXXXXXXX    XXXXXXXXXXX
  #XXXXXXXX#    XXXXXXXXXXX
                #XXXXXXXXX#

'''
TEST_INPUT_HOLE = '''1,2
27,2
27,12
17,12
17,9
13,9
13,6
21,6
21,4
12,4
12,11
3,11
3,9
1,9
'''


def run_tests_hole():
    tiles = parse_tiles(TEST_INPUT_HOLE)
    vert_lines, horiz_lines = get_lines(tiles)
    print(vert_lines)
    print(horiz_lines)
    assert(is_square_tiled((3, 11), (12, 4), horiz_lines, vert_lines))
    assert(is_square_tiled((27, 12), (17, 9), horiz_lines, vert_lines))
    assert(is_square_tiled((27, 12), (21, 6), horiz_lines, vert_lines))
    assert(not is_square_tiled((27, 12), (13, 6), horiz_lines, vert_lines))
    assert(is_square_tiled((1, 2), (12, 4), horiz_lines, vert_lines))
    assert(not is_square_tiled((1, 2), (13, 6), horiz_lines, vert_lines))
    assert(not is_square_tiled((1, 2), (21, 6), horiz_lines, vert_lines))
    assert(is_square_tiled((1, 9), (21, 8), horiz_lines, vert_lines))
    assert(is_line_tiled(8, 9, 12, horiz_lines))
    assert(is_square_tiled((1, 9), (21, 6), horiz_lines, vert_lines))
    assert(not is_square_tiled((1, 9), (21, 4), horiz_lines, vert_lines))
    assert(is_line_tiled(4, 9, 12, horiz_lines))
    assert(is_square_tiled((1, 9), (12, 4), horiz_lines, vert_lines))
    assert(is_line_tiled(17, 21, 6, vert_lines))
    assert(is_square_tiled((21, 6), (17, 12), horiz_lines, vert_lines))
    print(solve_pt2(tiles))


if __name__ == '__main__':
    main()
