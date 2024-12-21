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
            return [r + d, d + r]
        elif dx >= 0 and dy < 0:
            l = '<' * (-1 * dy)
            d = 'v' * dx
            return [l + d, d + l]
        elif dx < 0 and dy >= 0:
            r = '>' * dy
            u = '^' * (-1 * dx)
            return [r + u, u + r]
        elif dx < 0 and dy < 0:
            l = '<' * (-1 * dy)
            u = '^' * (-1 * dx)
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
    return sum([
        get_presses_to_enter(result, keyboard)
        for result in results
    ], [])

def get_robot1_presses(result):
    return get_presses_to_enter_alts([result], NUM_KEYBOARD)

def get_robot2_presses(result):
    return get_presses_to_enter_alts(get_robot1_presses(result), ARROW_KEYBOARD)

def get_your_presses(result):
    return get_presses_to_enter_alts(get_robot2_presses(result), ARROW_KEYBOARD)


def get_your_shortest_press(to_enter):
    min_len = float('inf')
    result = None
    for press in get_your_presses(to_enter):
        if len(press) >= min_len:
            continue
        min_len = len(press)
        result = press
    return result


def get_score(code):
    num_part = int(code[:-1])
    your_presses = min(map(len, get_your_presses(code)))
    print(num_part, your_presses)
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
    # print(get_your_presses(the_test))
    shortest = [
        get_your_shortest_press(code) for code in test_input
    ]
    for s, c in zip(shortest, test_input):
        print(s, c, play_all_presses(s))
    scores = [
        get_score(code) for code in test_input
    ]
    print(scores)
    print(sum(scores))
    # print(BETTER_LAST_PRESS)
    # robot2_press = play_presses(BETTER_LAST_PRESS, ARROW_KEYBOARD)
    # print(robot2_press)
    # robot1_press = play_presses(robot2_press, ARROW_KEYBOARD)
    # print(robot1_press)
    # actual_press = play_presses(robot1_press, NUM_KEYBOARD)
    # print(actual_press)
    # print(get_robot1_presses(actual_press))
    # print(get_robot2_presses(actual_press))
    # print(get_your_presses(actual_press))


if __name__ == '__main__':
    main()
