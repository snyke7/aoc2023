from utils import add_coord, DIRECTIONS2, UP2, DOWN2, LEFT2, RIGHT2


TEST_INPUT = '''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''


def read_coords(map_str):
    return {
        (i, j)
        for i, line in enumerate(map_str.splitlines())
        for j, el in enumerate(line.strip())
        if el == '@'
    }


ADJACENT2 = DIRECTIONS2 + [
    add_coord(DIRECTIONS2[i], DIRECTIONS2[(i + 1) % 4])
    for i in range(len(DIRECTIONS2))
]


def get_neighbors(c):
    return [
        add_coord(c, adj)
        for adj in ADJACENT2
    ]


def is_reachable(c, coords):
    return len(set(get_neighbors(c)) & coords) < 4


def get_reachable(coords):
    return {c for c in coords if is_reachable(c, coords)}


def count_reachable(coords):
    return len(get_reachable(coords))


def count_reachable_multi_step(coords):
    state = set(coords)
    progress = True
    while progress:
        to_remove = get_reachable(state)
        state.difference_update(to_remove)
        progress = len(to_remove) > 0
    return len(coords) - len(state)


def main():
    map_coords = read_coords(TEST_INPUT)
    print(count_reachable(map_coords))
    print(count_reachable_multi_step(map_coords))
    with open('input/day04.txt') as f:
        map_coords = read_coords(f.read())
    print(count_reachable(map_coords))
    print(count_reachable_multi_step(map_coords))


if __name__ == '__main__':
    main()
