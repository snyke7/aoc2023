def to_index_path(path):
    return [0 if p == 'L' else 1 for p in path]


def parse_node_map(map_lines):
    result = {}
    for line in map_lines:
        node, _, dests = line.partition('=')
        node = node.strip()
        dest_list = dests.strip()[1:-1].split(', ')
        result[node] = dest_list
    return result


def count_steps_to(the_map, the_path, the_start, the_dest, min_steps=0):
    steps = 0
    loc = the_start
    while loc != the_dest or steps < min_steps:
        loc = the_map[loc][the_path[steps % len(the_path)]]
        steps += 1
    return steps


def do_steps(the_map, the_path, the_start, max_steps):
    steps = 0
    loc = the_start
    history = [loc]
    while steps < max_steps:
        loc = the_map[loc][the_path[steps % len(the_path)]]
        steps += 1
        history.append(loc)
    return loc, history


def count_simultaneous_steps_to(the_map, the_path, start_tail_letter, end_tail_letter):
    steps = 0
    locs = {node for node in the_map.keys() if node.endswith(start_tail_letter)}
    print(len(locs))
    while any((not node.endswith(end_tail_letter) for node in locs)):
        locs = {the_map[loc][the_path[steps % len(the_path)]] for loc in locs}
        print(locs)
        steps += 1
        if steps % 1000000 == 999999:
            print(steps)
    return steps


def find_loops_in_path(the_map, the_path, start):
    idx_map = {0: {start: 0}}
    loc = start
    steps = 0
    while True:
        offset = steps % len(the_path)
        loc = the_map[loc][the_path[offset]]
        steps += 1
        if offset not in idx_map:
            idx_map[offset] = {loc: steps}
        else:
            if loc in idx_map[offset]:
                # found loop!
                return steps, loc, idx_map[offset][loc]
            else:
                idx_map[offset][loc] = steps


def make_quick_step_calc(the_map, path, start):
    steps, loop_node, prev_steps = find_loops_in_path(the_map, path, start)
    loop_length = steps - prev_steps
    path_circ = path[steps % len(path):] + path[:steps % len(path)]
    head_step_history = do_steps(the_map, path, start, steps)[1]
    circ_step_history = do_steps(the_map, path_circ, loop_node, loop_length)[1]

    def shortcut(the_steps):
        if the_steps <= steps:
            return head_step_history[the_steps]
        else:
            offset_steps = (the_steps - steps) % loop_length
            return circ_step_history[offset_steps]
    return shortcut, steps, loop_length


def find_simultaneous_letters(the_map, path, start_nodes):
    fast_calcs = list(sorted(
        [make_quick_step_calc(the_map, path, node) for node in start_nodes],
        key=lambda pr: pr[1]
    ))
    step_fun, head_length, loop_length = fast_calcs.pop()
    # get the node with the largest head_length

    # check if there is an overlap in the beginning (probably not since brute-force failed :))
    for j in range(head_length):
        if step_fun(j).endswith('Z') and all((
                other_step(j).endswith('Z')
                for other_step, _, _ in fast_calcs
        )):
            return j

    # find it in a better way
    offsets = [i for i in range(loop_length) if step_fun(head_length + i).endswith('Z')]
    n = 0
    while True:
        for i in offsets:
            if all((other_step(head_length + n * loop_length + i).endswith('Z')
                    for other_step, _, _ in fast_calcs)):
                return head_length + n * loop_length + i
        n += 1
        if n % 100 == 99:
            print(head_length + n * loop_length)


def check_simultaneous_letters(the_map, path, start_nodes, steps):
    print(start_nodes)
    fast_steps = [make_quick_step_calc(the_map, path, node)[0](steps) for node in start_nodes]
    print(fast_steps)


def main():
    with open('input/day08_input.txt') as f:
        all_lines = f.readlines()
    all_lines2 = '''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)'''.splitlines()
    all_lines3 = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''.splitlines()
    all_lines4 = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''.splitlines()
    path = to_index_path(all_lines[0].strip())
    the_map = parse_node_map(all_lines[2:])
    # print(count_steps_to(the_map, path, 'MJA', '11Z'))

    print(find_simultaneous_letters(the_map, path, [node for node in the_map.keys() if node.endswith('A')]))
    # 21003205388413
    # print(check_simultaneous_letters(the_map, path,
    #                                  [node for node in the_map.keys() if node.endswith('A')][:6], 21003205388413))


if __name__ == '__main__':
    main()
