from utils import *


# TAGS:
#trivial


def get_area(present):
    l, w, h = present
    slack = min(l * w, w * h, h * l)
    return 2 * (l * w + w * h + h * l) + slack


def get_ribbon_length(present):
    l, w, h = present
    perimeter = 2 * sum(sorted(present)[:2])
    return perimeter + l * w * h


lines = file_read_lines('input/day02_input.txt')
presents = [tuple(map(int, line.split('x'))) for line in lines]
print(sum(map(get_area, presents)))
print(sum(map(get_ribbon_length, presents)))
