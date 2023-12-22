from utils import *


# TAGS:
#trivial


def is_nice_pt1(the_str: str) -> bool:
    vowels = [el for el in the_str if el in set('aeiou')]
    if len(vowels) < 3:
        return False
    bad_pairs = ['ab', 'cd', 'pq', 'xy']
    if any((pair in the_str for pair in bad_pairs)):
        return False
    for pair in zip(the_str[:-1], the_str[1:]):
        if len(set(pair)) == 1:
            return True
    return False


def is_nice_pt2(the_str: str) -> bool:
    found_pair = False
    found_sandwich = False
    for i in range(len(the_str) - 1):
        pair_cand = the_str[i:i + 2]
        if pair_cand in the_str[i+2:]:
            found_pair = True
        if i < len(the_str) - 2:
            if the_str[i] == the_str[i + 2]:
                found_sandwich = True
    return found_pair and found_sandwich


lines = file_read_lines('input/day05_input.txt')
print(len([line for line in lines if is_nice_pt1(line)]))
print(len([line for line in lines if is_nice_pt2(line)]))

# print(is_nice_pt2('qjhvhtzxzqqjkmpb'))
# print(is_nice_pt2('xxyxx'))
# print(is_nice_pt2('uurcxstgmygtbstg'))
# print(is_nice_pt2('ieodomkazucvgmuy'))
