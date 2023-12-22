from utils import *


# TAGS:
#strings
#annoying
#pythonbestparser
#pythonnotbestparser


TEST_raw = r'''""
"abc"
"aaa\"aaa"
"\x27"'''


def make_nice(the_str: str) -> str:
    result = ''
    is_escaping = False
    is_hex = False
    hex_val = None
    for i in range(1, len(the_str) - 1):
        if is_escaping:
            if the_str[i] == '\\':
                result += '\\'
            elif the_str[i] == r'"':
                result += r'"'
            elif the_str[i] == 'x':
                is_hex = True
            is_escaping = False
        elif is_hex:
            if hex_val is None:
                hex_val = the_str[i]
            else:
                result += chr(int(hex_val + the_str[i], 16))
                hex_val = None
                is_hex = False
        elif the_str[i] != '\\':
            result += the_str[i]
        else:
            is_escaping = True
    return result


def escape(the_str: str) -> str:
    return '"' + the_str.replace('\\', '\\\\').replace('"', '\\"') + '"'


lines = file_read_lines('input/day08_input.txt')
lines2 = TEST_raw.splitlines()
nice_lines = [make_nice(line) for line in lines]

print(sum(map(len, lines)) - sum(map(len, nice_lines)))
print(sum(map(len, map(escape, lines))) - sum(map(len, lines)))
