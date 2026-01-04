from utils import DIRECTIONS2, add_coord


NEIGHBORS2 = DIRECTIONS2 + [add_coord(prev, nxt) for prev, nxt in zip(DIRECTIONS2, DIRECTIONS2[1:] + [DIRECTIONS2[0]])]

TEST_INPUT = '''.#.#.#
...##.
#....#
..#...
#.#..#
####..
'''


def read_lights(light_str):
    return {
        (i, j): el == '#'
        for i, line in enumerate(light_str.splitlines())
        for j, el in enumerate(line.strip())
    }


def count_lit_neighbors(lights, pos):
    return len([
        lights[neighbor]
        for neighbor in (add_coord(pos, n) for n in NEIGHBORS2)
        if neighbor in lights and lights[neighbor]
    ])


def get_next_light_val(is_lit, lit_neighbors):
    if is_lit:
        return lit_neighbors in {2, 3}
    else:
        return lit_neighbors == 3


def turn_on_corners(lights):
    i_max = max((i for i, _ in lights.keys()))
    j_max = max((j for _, j in lights.keys()))
    lights[(0, 0)] = True
    lights[(0, j_max)] = True
    lights[(i_max, 0)] = True
    lights[(i_max, j_max)] = True


def game_of_light_iter(prev_lights, corners=False):
    result = {
        pos: get_next_light_val(val, count_lit_neighbors(prev_lights, pos))
        for pos, val in prev_lights.items()
    }
    if corners:
        turn_on_corners(result)
    return result


def to_light_str(light_dict):
    i_max = max((i for i, _ in light_dict.keys()))
    j_max = max((j for _, j in light_dict.keys()))
    return '\n'.join((
        ''.join((
            '#' if light_dict[(i, j)] else '.'
            for j in range(j_max + 1)
        ))
        for i in range(i_max + 1)
    ))


def main():
    test_input = TEST_INPUT
    with open('input/day18.txt') as f:
        test_input = f.read()

    cur_lights = read_lights(test_input)
    turn_on_corners(cur_lights)

    num_iters = 4
    num_iters = 5
    num_iters = 100

    for i in range(num_iters):
        cur_lights = game_of_light_iter(cur_lights, corners=True)
        # print(to_light_str(cur_lights))
        # print()
    print(len([1 for val in cur_lights.values() if val]))


if __name__ == '__main__':
    main()
