from utils import *


# TAGS:
#trivial
#grid2d


MOVE_MAP = {
    '^': UP2,
    'v': DOWN2,
    '>': RIGHT2,
    '<': LEFT2
}


def get_path(direction_str: str) -> List[Coord2]:
    cur_pos = (0, 0)
    result = [cur_pos]
    for el in direction_str:
        cur_pos = add_coord(cur_pos, MOVE_MAP[el])
        result.append(cur_pos)
    return result


line = file_read_lines('input/day03_input.txt')[0]
path = get_path(line)
print(len(set(path)))
path1 = get_path(line[::2])
path2 = get_path(line[1::2])
print(len(set(path1) | set(path2)))
