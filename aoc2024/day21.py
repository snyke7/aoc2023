from itertools import product

from utils import sub_coord, add_coord, UP2, RIGHT2, DOWN2, LEFT2


TEST_INPUT = '''029A
980A
179A
456A
379A
'''

BETTER_LAST_PRESS = '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'

REAL_INPUT = '''985A
540A
463A
671A
382A
'''


NUM_KEYBOARD = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                 '0': (3, 1), 'A': (3, 2),
}

ARROW_KEYBOARD = {
                 '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}

MOVE_DICT = {
    '^': UP2, '>': RIGHT2, 'v': DOWN2, '<': LEFT2,
}


def get_paths(keyboard, from_el, to_el):
    from_c = keyboard[from_el]
    to_c = keyboard[to_el]
    dx, dy = sub_coord(to_c, from_c)
    if dy == 0:
        return ['v' * max(0, dx) + '^' * (-1 * min(0, dx))]
    elif dx == 0:
        return ['>' * max(0, dy) + '<' * (-1 * min(0, dy))]
    else:
        if dx >= 0 and dy >= 0:
            r = '>' * dy
            d  = 'v' * dx
            # if is_path_safe(d + r, from_el, keyboard):
            #     return [d + r]
            # return [r + d]
            return [r + d, d + r]
        elif dx >= 0 and dy < 0:
            l = '<' * (-1 * dy)
            d = 'v' * dx
            # if is_path_safe(l + d, from_el, keyboard):
            #     return [l + d]
            return [l + d, d + l]
        elif dx < 0 and dy >= 0:
            r = '>' * dy
            u = '^' * (-1 * dx)
            # if is_path_safe(r + u, from_el, keyboard):
            #     return [r + u]
            # return [u + r]
            return [r + u, u + r]
        elif dx < 0 and dy < 0:
            l = '<' * (-1 * dy)
            u = '^' * (-1 * dx)
            # if is_path_safe(l + u, from_el, keyboard):
            #     return [l + u]
            return [l + u, u + l]


def is_path_safe(path, from_el, keyboard):
    rev_keyboard = {v: k for k, v in keyboard.items()}
    cur_pos = keyboard[from_el]
    for press in path:
        cur_pos = add_coord(cur_pos, MOVE_DICT[press])
        # cannot hover over gap
        if cur_pos not in rev_keyboard:
            return False
    return True


def get_safe_paths(keyboard, from_el, to_el):
    return [
        path
        for path in get_paths(keyboard, from_el, to_el)
        if is_path_safe(path, from_el, keyboard)
    ]


def get_presses_to_enter(result, keyboard):
    connections = [
        [path + 'A' for path in get_safe_paths(keyboard, from_el, to_el)]
        for from_el, to_el in
        zip('A' + result, result)
    ]
    return [''.join(prod) for prod in product(*connections)]


def get_presses_to_enter_alts(results, keyboard):
    return filter_shortest(sum([
        get_presses_to_enter(result, keyboard)
        for result in results
    ], []))

def get_robot1_presses(result):
    return get_presses_to_enter_alts([result], NUM_KEYBOARD)

def get_robot2_presses(result):
    return get_presses_to_enter_alts(get_robot1_presses(result), ARROW_KEYBOARD)

def get_your_presses(result):
    return get_presses_to_enter_alts(get_robot2_presses(result), ARROW_KEYBOARD)


def get_your_presses_pt2(to_enter, intermediate_robot_count):
    result = get_robot1_presses(to_enter)
    for i in range(intermediate_robot_count):
        # print(i, len(result))
        result = get_presses_to_enter_alts(result, ARROW_KEYBOARD)
    return result


def count_your_presses(to_enter, intermediate_robot_count):
    to_enter = get_robot1_presses(to_enter)
    key_move_and_enter_count = {
        (key1, key2): 1  # move costs nothing, entering key2 costs 1
        for key1 in ARROW_KEYBOARD.keys()
        for key2 in ARROW_KEYBOARD.keys()
    }
# <  ->  ^
# becomes
# A  >^  A
# becomes
# A -> > -> ^ -> A
# A v  A <^ A >  A
    def read_new_move_count(path_opts):
        return min((sum((
            key_move_and_enter_count[(prev_key, next_key)]
            for prev_key, next_key in zip(
                'A' + path, path
            )
        )) for path in path_opts))
    for _ in range(intermediate_robot_count):
        key_move_and_enter_count = {
            (key1, key2): read_new_move_count([
                path + 'A'
                for path in get_safe_paths(ARROW_KEYBOARD, key1, key2)
            ])
            for key1 in ARROW_KEYBOARD.keys()
            for key2 in ARROW_KEYBOARD.keys()
        }
    return read_new_move_count(to_enter)


def get_score_fast(code, intermediate_robot_count):
    num_part = int(code[:-1])
    your_presses = count_your_presses(code, intermediate_robot_count)
    return num_part * your_presses


def filter_shortest(sequence):
    min_len = float('inf')
    result = []
    for press in sequence:
        if len(press) > min_len:
            continue
        if len(press) < min_len:
            result = []
            min_len = len(press)
        result.append(press)
    return result


def get_your_shortest_presses(to_enter):
    min_len = float('inf')
    result = []
    for press in get_your_presses(to_enter):
        if len(press) > min_len:
            continue
        if len(press) < min_len:
            result = []
            min_len = len(press)
        result.append(press)
    return result


def get_score(code):
    num_part = int(code[:-1])
    your_presses = min(map(len, get_your_presses(code)))
    return num_part * your_presses


def play_presses(presses, keyboard):
    rev_keyboard = {v: k for k, v in keyboard.items()}
    cur_pos = keyboard['A']
    result = ''
    for press in presses:
        if press == 'A':
            result += rev_keyboard[cur_pos]
        else:
            cur_pos = add_coord(cur_pos, MOVE_DICT[press])
    return result


def play_all_presses(presses):
    robot2_press = play_presses(presses, ARROW_KEYBOARD)
    robot1_press = play_presses(robot2_press, ARROW_KEYBOARD)
    return play_presses(robot1_press, NUM_KEYBOARD)


def main():
    test_input = TEST_INPUT.splitlines()
    test_input = REAL_INPUT.splitlines()
    scores = [
        get_score_fast(code, 2) for code in test_input
    ]
    print(sum(scores))
    scores = [
        get_score_fast(code, 25) for code in test_input
    ]
    print(sum(scores))


if __name__ == '__main__':
    main()

# thoughts: bottom up construction!!

# <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# <A>Av<<AA>^AA>AvAA^A<vAAA>^A
# ^A<<^^A>>AvvvA
# 379A
# ^A^^<<A>>AvvvA
# <A>A<AAv<AA^>>AvAA^Av<AAA^>A
# v<<A^>>AvA^Av<<A^>>AAv<A<A^>>AA<A>vAA^Av<A^>AA<A>Av<A<A^>>AAA<A>vA^A
#
#
# 379A
# ^A   ^^<< A>>AvvvA
# ^A   <<^^ A>>AvvvA
# <A>A <AAv<AA^>>                        AvAA^A        v<       AAA^>A
# <A>A v<<AA>^AA>                        AvAA^A        <v       AAA>^A
# v<<A^>>AvA^A v<<A^>>AAv<A<A^>>AA<A>vAA ^Av<A^>AA<A>Av<A<A  ^>>AAA<A>vA^A
# <v<A>>^AvA^A <vA<AA>>^AAvA<^A>AAvA     ^A<vA>^AA<A>A<v<A>A  >^AAAvA<^A>A
#
# 3 -> 7
# <<^^A
# < -> ^
# >^A
# > -> ^
# <^A
#
# every pair maps to a sequence (of pairs)
#
# bottom up instead of top down?
#
# > -> ^ in 1 =
# <^A = 3
#
# < -> ^ in 2 =
# >^A in 1 =
# 1 + (> -> ^ in 1) + 1 + (^ -> A in 1) + 1



