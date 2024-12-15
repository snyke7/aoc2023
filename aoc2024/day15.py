from utils import DIRECTIONS2, add_coord, UP2, RIGHT2, DOWN2, LEFT2


TEST_INPUT1 = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''

TEST_INPUT2 = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
'''

TEST_INPUT3 = '''#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
'''


MOVE_DICT = {
    '^': UP2,
    '>': RIGHT2,
    'v': DOWN2,
    '<': LEFT2,
}

EMPTY = 0
BOX = 1
WALL = 2
ROBOT = 3
BOX_LEFT = 4
BOX_RIGHT = 5
MAP_DICT = {
    '.': EMPTY,
    'O': BOX,
    '#': WALL,
    '@': ROBOT,
    '[': BOX_LEFT,
    ']': BOX_RIGHT,
}
MAP_BICT_BACK = {
    EMPTY: '.',
    BOX: 'O',
    WALL: '#',
    ROBOT: '@',
    BOX_LEFT: '[',
    BOX_RIGHT: ']',
}


def parse_input_lines(input_lines):
    warehouse_str, _, moves_str = input_lines.partition('\n\n')
    moves = [MOVE_DICT[el] for el in moves_str if el != '\n']
    warehouse = {
        (i, j): MAP_DICT[el]
        for i, line in enumerate(warehouse_str.split('\n'))
        for j, el in enumerate(line.strip())
    }
    warehouse_pt2 = {}
    for (i, j), el in warehouse.items():
        if el in {EMPTY, WALL}:
            warehouse_pt2[(i, 2 * j)] = el
            warehouse_pt2[(i, 2 * j + 1)] = el
        elif el == BOX:
            warehouse_pt2[(i, 2 * j)] = BOX_LEFT
            warehouse_pt2[(i, 2 * j + 1)] = BOX_RIGHT
        elif el == ROBOT:
            warehouse_pt2[(i, 2 * j)] = ROBOT
            warehouse_pt2[(i, 2 * j + 1)] = EMPTY
    robot_pos = None
    robot_pos2 = None
    for c, el in list(warehouse.items()):
        if el == ROBOT:
            robot_pos = c
            robot_pos2 = (c[0], 2 * c[1])
            break
    return warehouse, moves, robot_pos, warehouse_pt2, robot_pos2


def get_boxes_to_move(warehouse, robot_pos, direction):
    cur_pos = robot_pos
    to_move = []
    while True:
        cur_pos = add_coord(cur_pos, direction)
        to_move.append(cur_pos)
        if cur_pos not in warehouse:
            raise Exception('Programming error!')
        if warehouse[cur_pos] == WALL:
            return []
        elif warehouse[cur_pos] == EMPTY:
            return to_move
        elif warehouse[cur_pos] == BOX:
            pass

def move_robot(warehouse, robot_pos, direction):
    to_move = get_boxes_to_move(warehouse, robot_pos, direction)
    if not to_move:
        return robot_pos
    # to_move has elements: the last one is the free spot that will now be taken,
    # the first one is the spot that the robot will move to
    # box + 1, robot, empty - 1
    warehouse[to_move[-1]] = BOX
    # box, robot + 1, empty - 1
    warehouse[to_move[0]] = ROBOT
    # box, robot, empty
    warehouse[robot_pos] = EMPTY
    return to_move[0]


def get_boxes_to_move_pt2(warehouse, robot_pos, direction):
    moving_positions = {robot_pos: EMPTY}
    move_dict = {}
    while moving_positions:
        cur_pos = next(iter(moving_positions))
        prev_el = moving_positions.pop(cur_pos)
        move_dict[cur_pos] = prev_el
        if cur_pos not in warehouse:
            raise Exception('Programming error!')
        if warehouse[cur_pos] == WALL:
            return {}
        if warehouse[cur_pos] == EMPTY:
            continue
        new_pos = add_coord(cur_pos, direction)
        # following may overwrite an EMPTY, as desired
        moving_positions[new_pos] = warehouse[cur_pos]
        if direction[0] == 0:
            continue
        if warehouse[new_pos] == BOX_LEFT:
            # we are running this BFS. so next row is executed after current row is completely finished
            left_box_pos = (new_pos[0], new_pos[1] + 1)
            if left_box_pos not in moving_positions:
                moving_positions[left_box_pos] = EMPTY
        elif warehouse[new_pos] == BOX_RIGHT:
            # we are running this BFS. so next row is executed after current row is completely finished
            right_box_pos = (new_pos[0], new_pos[1] - 1)
            if right_box_pos not in moving_positions:
                moving_positions[right_box_pos] = EMPTY
    return move_dict


def move_robot_pt2(warehouse, robot_pos, direction):
    to_move = get_boxes_to_move_pt2(warehouse, robot_pos, direction)
    if not to_move:
        return robot_pos
    new_robot_pos = None
    for c, el in to_move.items():
        warehouse[c] = el
        if el == ROBOT:
            new_robot_pos = c
    return new_robot_pos


def warehouse_to_str(warehouse):
    max_row = max(map(lambda pr: pr[0], warehouse.keys()))
    max_col = max(map(lambda pr: pr[1], warehouse.keys()))
    return '\n'.join((
        ''.join((
            MAP_BICT_BACK[warehouse[(i, j)]]
            for j in range(max_col + 1)
        ))
        for i in range(max_row + 1)
    ))


def move_all_robot(warehouse, robot, moves):
    for move in moves:
        robot = move_robot(warehouse, robot, move)
    return robot


def get_gps_value(coord):
    return 100 * coord[0] + coord[1]


def move_all_robot_pt2(warehouse, robot, moves):
    for move in moves:
        robot = move_robot_pt2(warehouse, robot, move)
    return robot


def main():
    test_input = TEST_INPUT1
    with open('input/day15.txt') as f:
        test_input = f.read()
    warehouse, moves, robot, warehouse2, robot2 = parse_input_lines(test_input)
    robot = move_all_robot(warehouse, robot, moves)
    print(sum((
        get_gps_value(c)
        for c, el in warehouse.items()
        if el == BOX
    )))
    robot2 = move_all_robot_pt2(warehouse2, robot2, moves)
    print(sum((
        get_gps_value(c)
        for c, el in warehouse2.items()
        if el == BOX_LEFT
    )))



if __name__ == '__main__':
    main()
