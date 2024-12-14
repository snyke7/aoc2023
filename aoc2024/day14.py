import click


TEST_INPUT = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''


def read_2tuple(tup_str):
    return tuple(map(int, reversed(tup_str.split(','))))


def read_pos_and_vel(robot_str):
    pos_str, _, vel_str = robot_str.partition(' ')
    return read_2tuple(pos_str.partition('=')[2]), read_2tuple(vel_str.partition('=')[2])


def calc_dest(robot_pos, robot_vel, steps, dimensions):
    return (
        (robot_pos[0] + robot_vel[0] * steps) % dimensions[0],
        (robot_pos[1] + robot_vel[1] * steps) % dimensions[1],
    )


def calc_safetyfactor(robot_positions, dimensions):
    qs = [[0, 0], [0, 0]]
    for x, y in robot_positions:
        if 2 * x + 1 == dimensions[0]:
            continue
        if 2 * y + 1 == dimensions[1]:
            continue
        qs[x // (dimensions[0] // 2 + 1)][y // (dimensions[1] // 2 + 1)] += 1
    return qs[0][0] * qs[0][1] * qs[1][0] * qs[1][1]


def positions_to_str(robot_positions, dimensions):
    return '\n'.join((
        ''.join((
            str(robot_positions.count((x, y)))
            if (x, y) in robot_positions else '.'
            for y in range(dimensions[1])
        ))
        for x in range(dimensions[0])
    ))


def calc_entropy(robot_positions, dimensions, granularity):
    quads = []
    for i in range(granularity):
        quads.append([0] * granularity)
    for x, y in robot_positions:
        quadx_i = x // (dimensions[0] // granularity + 1)
        quady_i = y // (dimensions[1] // granularity + 1)
        quads[quadx_i][quady_i] += 1
    avg = len(robot_positions) / (granularity ** 2)
    return sum((abs(quad - avg) for quad in sum(quads, [])))


def main():
    test_input, dims = TEST_INPUT.splitlines(), (7, 11)
    with open('input/day14.txt') as f:
        test_input, dims = f.readlines(), (103, 101)
    robots = [read_pos_and_vel(robot_str.strip()) for robot_str in test_input]
    robot_positions = [calc_dest(pos, vel, 100, dims) for pos, vel in robots]
    print(calc_safetyfactor(robot_positions, dims))
    print()
    do_continue = True
    steps = 50
    while do_continue:
        robot_positions = [calc_dest(pos, vel, steps, dims) for pos, vel in robots]
        entropy = calc_entropy(robot_positions, dims, 3)
        if entropy < 500:
            # print(f'Steps: {steps}, "entropy3": {entropy}')
            do_continue = True
        else:
            print(positions_to_str(robot_positions, dims))
            print(f'Steps: {steps}, "entropy3": {entropy}')
            # do_continue = click.confirm('Another?', default=True)
            do_continue = False
        steps += 1


if __name__ == '__main__':
    main()
