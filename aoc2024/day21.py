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


def get_path(keyboard, from_el, to_el):
    from_c = keyboard[from_el]
    to_c = keyboard[to_el]
    dx, dy = sub_coord(to_c, from_c)
    if dx >= 0 and dy >= 0:
        return '>' * dy + 'v' * dx
    elif dx >= 0 and dy < 0:
        return 'v' * dx + '<' * (-1 * dy)
    elif dx < 0 and dy >= 0:
        return '^' * (-1 * dx) + '>' * dy
    elif dx < 0 and dy < 0:
        return '^' * (-1 * dx) + '<' * (-1 * dy)


def get_presses_to_enter(result, keyboard):
    return ''.join((
        get_path(keyboard, from_el, to_el) + 'A'
        for from_el, to_el in
        zip('A' + result, result)
    ))


def get_robot1_presses(result):
    return get_presses_to_enter(result, NUM_KEYBOARD)

def get_robot2_presses(result):
    return get_presses_to_enter(get_robot1_presses(result), ARROW_KEYBOARD)

def get_your_presses(result):
    return get_presses_to_enter(get_robot2_presses(result), ARROW_KEYBOARD)


def get_score(code):
    num_part = int(code[:-1])
    your_presses = len(get_your_presses(code))
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


def main():
    test_input = TEST_INPUT.splitlines()
    the_test = '379A'
    print(get_robot1_presses(the_test))
    print(get_robot2_presses(the_test))
    print(get_your_presses(the_test))
    scores = [
        get_score(code) for code in test_input
    ]
    print(scores)
    print(sum(scores))
    print(BETTER_LAST_PRESS)
    robot2_press = play_presses(BETTER_LAST_PRESS, ARROW_KEYBOARD)
    print(robot2_press)
    robot1_press = play_presses(robot2_press, ARROW_KEYBOARD)
    print(robot1_press)
    actual_press = play_presses(robot1_press, NUM_KEYBOARD)
    print(actual_press)
    print(get_robot1_presses(actual_press))
    print(get_robot2_presses(actual_press))
    print(get_your_presses(actual_press))


if __name__ == '__main__':
    main()
