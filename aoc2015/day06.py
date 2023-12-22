from utils import *
from collections import defaultdict


# TAGS:
#trivial
#grid2d
#range2d


lines = file_read_lines('input/day06_input.txt')
lines2 = [
    'turn on 0,0 through 999,999',
    'toggle 0,0 through 999,0',
    'turn off 499,499 through 500,500'
]
my_grid = defaultdict(lambda: False)

is_part2 = True


def parse_coord2(raw: str) -> Coord2:
    return tuple(map(int, raw.split(',')))


for line in lines:
    if line.startswith('toggle '):
        head = 'toggle '
        action = (lambda o: not o) if not is_part2 else (lambda o: o + 2)
    elif line.startswith('turn on '):
        head = 'turn on '
        action = (lambda o: True) if not is_part2 else (lambda o: o + 1)
    elif line.startswith('turn off '):
        head = 'turn off '
        action = (lambda o: False) if not is_part2 else (lambda o: max(0, o - 1))
    else:
        raise ValueError(line)
    left_r, _, right_r = line[len(head):].partition(' through ')
    left = parse_coord2(left_r)
    right = parse_coord2(right_r)
    for x in range(left[0], right[0] + 1):
        for y in range(left[1], right[1] + 1):
            my_grid[(x, y)] = action(my_grid[(x, y)])


if not is_part2:
    print(len([(x, y) for (x, y), val in my_grid.items() if val]))
else:
    print(sum((val for val in my_grid.values())))
