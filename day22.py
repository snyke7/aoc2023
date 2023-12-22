from typing import Tuple, Set, Dict, List, Generator, Iterable
from collections import defaultdict

Cube = Tuple[int, int, int]
Rectangle = Tuple[Cube, Cube]


TEST = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''


def gen_neighbors(cube: Cube):
    x, y, z = cube
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y - 1, z
    yield x, y + 1, z
    yield x, y, z - 1
    yield x, y, z + 1


def count_side(cube: Cube, cubes: Set[Cube], interior):
    return sum((1 for neighbor in gen_neighbors(cube)
                if neighbor not in cubes and (interior is None or neighbor not in interior)))


def count_sides(cubes: Set[Cube], interior=None):
    return sum((count_side(cube, cubes, interior=interior) for cube in cubes))


def get_min_bb_cube(cubes: List[Cube]) -> Cube:
    minx = min((x for x, _, _ in cubes))
    miny = min((y for _, y, _ in cubes))
    minz = min((z for _, _, z in cubes))
    return minx, miny, minz


def get_max_bb_cube(cubes: List[Cube]) -> Cube:
    maxx = max((x for x, _, _ in cubes))
    maxy = max((y for _, y, _ in cubes))
    maxz = max((z for _, _, z in cubes))
    return maxx, maxy, maxz


def rectangle_iter(left: Cube, right: Cube) -> Generator[Cube, None, None]:
    minx, miny, minz = get_min_bb_cube([left, right])
    maxx, maxy, maxz = get_max_bb_cube([left, right])
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            for z in range(minz, maxz + 1):
                yield x, y, z


def in_bound(min_cube: Cube, max_cube: Cube, the_cube: Cube) -> bool:
    minx, miny, minz = min_cube
    maxx, maxy, maxz = max_cube
    x, y, z = the_cube
    return (minx <= x <= maxx and
            miny <= y <= maxy and
            minz <= z <= maxz)


def parse_cube(cube_str) -> Cube:
    return tuple(map(int, cube_str.split(',')))


def parse_cube_pair(line):
    left, _, right = line.strip().partition('~')
    return parse_cube(left), parse_cube(right)


def overlap(rectangle1, rectangle2):
    l1, r1 = rectangle1
    l2, r2 = rectangle2
    shared_coords = set(enumerate(l1)) & set(enumerate(l2))
    if len(shared_coords) < 1:
        return False
    elif len(shared_coords) == 3:
        return True
    cubes1 = set(rectangle_iter(l1, r1))
    cubes2 = set(rectangle_iter(l2, r2))
    return bool(cubes1 & cubes2)


def move_down(rect: Rectangle) -> Rectangle:
    return (rect[0][0], rect[0][1], rect[0][2] - 1), (rect[1][0], rect[1][1], rect[1][2] - 1)


def get_down_touching(rects_on_ground: Iterable[Rectangle], rect: Rectangle):
    down_rect = move_down(rect)
    return (rect for rect in rects_on_ground if overlap(down_rect, rect))


def touches_ground(rects_on_ground: Iterable[Rectangle], rect: Rectangle):
    if min(rect[0][2], rect[1][2]) == 1:
        return True
    return any((True for _ in get_down_touching(rects_on_ground, rect)))


def fall_down(rectangles: List[Rectangle], verbose=False):
    highest_z = defaultdict(lambda: 0)
    on_ground = []
    falling = sorted(rectangles, key=lambda pr: -1 * min(pr[0][2], pr[1][2]))
    time = 0
    falls = 0

    def do_drop(rect):
        falling.remove(rect)
        my_caused_falls = 0
        counted_my_fall = False
        while True:
            touch_ground = False
            for x, y, z in rectangle_iter(*rect):
                if highest_z[(x, y)] + 1 == z:
                    touch_ground = True
                    break
            if touch_ground:
                for x, y, z in rectangle_iter(*rect):
                    highest_z[(x, y)] = max(highest_z[(x, y)], z)
                on_ground.append(rect)
                return my_caused_falls
            rect = move_down(rect)
            if not counted_my_fall:
                my_caused_falls += 1
                counted_my_fall = True

    while falling:
        falls += do_drop(falling[-1])
        time += 1
        if time % 100 == 99 and verbose:
            print(time, len(falling))
    return on_ground, falls


def build_support_map(fallen_rectangles: List[Rectangle]):
    touch_down = {}
    touch_up = {}
    for rect in fallen_rectangles:
        touch_down[rect] = list(get_down_touching(set(fallen_rectangles) ^ {rect}, rect))
        for down_rect in touch_down[rect]:
            if down_rect not in touch_up:
                touch_up[down_rect] = []
            touch_up[down_rect].append(rect)
    return touch_down, touch_up


def construct_pyramid_from(base, touch_up, touch_down):
    to_add = base
    upward_pyramid = set(base)
    while to_add:
        add_now = to_add.pop()
        if add_now not in touch_up:
            continue
        for touch in touch_up[add_now]:
            if touch not in upward_pyramid:
                upward_pyramid.add(touch)
                to_add.append(touch)

    downward_pyramid = upward_pyramid.copy()
    to_add = list(upward_pyramid)
    while to_add:
        add_now = to_add.pop()
        for touch in touch_down[add_now]:
            if touch not in downward_pyramid:
                downward_pyramid.add(touch)
                to_add.append(touch)
    return downward_pyramid


def main():
    with open('input/day22_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    cube_pairs = [
        parse_cube_pair(line)
        for line in input_lines
    ]
    fallen, _ = fall_down(cube_pairs, verbose=False)
    touch_down, touch_up = build_support_map(fallen)
    safe_disintegrable = [
        rect for rect in fallen if
        all(
            bool(set(touch_down[up_rect]) ^ {rect})
            for up_rect in (touch_up[rect] if rect in touch_up else [])
        )
    ]
    print(len(safe_disintegrable))

    result = 0
    to_disintegrate = [rect for rect in fallen if rect not in safe_disintegrable]
    for the_rect in to_disintegrate:
        unsafe_fall_rects = list(construct_pyramid_from([the_rect], touch_up, touch_down))
        unsafe_fall_rects.remove(the_rect)
        _, unsafe_falls = fall_down(unsafe_fall_rects)
        # print(f'Disintegrating {the_rect} -> caused {unsafe_falls} falls')
        result += unsafe_falls
    print(f'{result}')  # < 80757


if __name__ == '__main__':
    main()
