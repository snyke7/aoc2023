from utils import *


# TAGS:
#trivial


def get_dest(the_str: str):
    return the_str.count('(') - the_str.count(')')


line = file_read_lines('input/day01_input.txt')[0]
print(get_dest(line))
print(next((
    i
    for i in range(len(line)) if
    get_dest(line[:i]) == -1
)))
