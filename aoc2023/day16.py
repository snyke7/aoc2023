TEST = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''


def parse_obstacles(input_lines):
    return {
        (i, j): el
        for i, line in enumerate(input_lines)
        for j, el in enumerate(line.strip())
        if el != '.'
    }


def beam_into(result_dict, obstacles, position, direction, size):
    x, y = position
    dy, dx = (1 - direction) if direction % 2 == 0 else 0, (2 - direction) if direction % 2 == 1 else 0
    steps = 0
    while ((x, y) not in obstacles or steps == 0) and 0 <= x < size and 0 <= y < size:
        if (x, y) not in result_dict:
            result_dict[(x, y)] = []
        if direction in result_dict[(x, y)]:
            return
        result_dict[(x, y)].append(direction)
        x += dx
        y += dy
        steps += 1
    if 0 <= x < size and 0 <= y < size:
        # hit obstacle
        handle_obstacle(result_dict, obstacles, (x, y), direction, size)


def handle_obstacle(result_dict, obstacles, position, direction, size):
    x, y = position
    obstacle = obstacles[(x, y)]
    if obstacle == '/':  # right0 -> up3, up3 -> right0, down1 -> left2, left2 -> down1
        new_dir = 3 if direction == 0 else (2 if direction == 1 else (1 if direction == 2 else 0))
        beam_into(result_dict, obstacles, (x, y), new_dir, size)
    elif obstacle == '\\':  # right0 -> down1, up3 -> left2, down1 -> right0, left2 -> up3
        new_dir = 1 if direction == 0 else (0 if direction == 1 else (3 if direction == 2 else 2))
        beam_into(result_dict, obstacles, (x, y), new_dir, size)
    elif obstacle == '|':
        if direction % 2 == 1:  # no split
            beam_into(result_dict, obstacles, (x, y), direction, size)
        else:  # do split
            beam_into(result_dict, obstacles, (x, y), 1, size)
            beam_into(result_dict, obstacles, (x, y), 3, size)
    elif obstacle == '-':
        if direction % 2 == 0:  # no split
            beam_into(result_dict, obstacles, (x, y), direction, size)
        else:  # do split
            beam_into(result_dict, obstacles, (x, y), 0, size)
            beam_into(result_dict, obstacles, (x, y), 2, size)


def beam_all_the_light(obstacles, start_pos, start_dir, size):
    result = {}  # position, direction dictionary
    if start_pos in obstacles:
        handle_obstacle(result, obstacles, start_pos, start_dir, size)
    else:
        beam_into(result, obstacles, start_pos, start_dir, size)
    return result


DIRECTION_STRING = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^'
}


def bounce_view(obstacles, beams, size):
    return '\n'.join(
        ''.join(
            obstacles[(i, j)] if (i, j) in obstacles else (
                '.' if (i, j) not in beams else (
                    DIRECTION_STRING[beams[(i, j)][0]]
                    if len(beams[(i, j)]) == 1 else (
                        str(len(beams[(i, j)]))
                    )
                )
            )
            for j in range (size)
        )
        for i in range(size)
    )


def find_best_beam(obstacles, size):
    max_beam = float('-inf')
    # top row
    for i in range(size):
        num_beams = len(beam_all_the_light(obstacles, (0, i), 1, size))
        if num_beams > max_beam:
            max_beam = num_beams

        num_beams = len(beam_all_the_light(obstacles, (size - 1, i), 3, size))
        if num_beams > max_beam:
            max_beam = num_beams

        num_beams = len(beam_all_the_light(obstacles, (i, 0), 0, size))
        if num_beams > max_beam:
            max_beam = num_beams

        num_beams = len(beam_all_the_light(obstacles, (i, size - 1), 2, size))
        if num_beams > max_beam:
            max_beam = num_beams

    return max_beam


def main():
    with open('input/day16_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    obstacles = parse_obstacles(input_lines)
    beams = beam_all_the_light(obstacles, (0, 0), 0, len(input_lines))
    # print(bounce_view(obstacles, beams, len(input_lines)))
    print(len(beams))
    print(find_best_beam(obstacles, len(input_lines)))


if __name__ == '__main__':
    main()
