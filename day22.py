from typing import Tuple, Set, Dict, List, Generator, Iterable

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
    # this is quite slow (~2 minutes with pypy), but is somewhat easy to understand
    on_ground = []
    falling = rectangles
    time = 0
    falls = 0

    def do_drop(rect):
        falling.remove(rect)
        my_falls = 0
        while True:
            if touches_ground(on_ground, rect):
                on_ground.append(rect)
                return my_falls
            touch_in_fall = list(get_down_touching(falling, rect))
            if not fall_touching:
                rect = move_down(rect)
                my_falls += 1
            else:
                minimum_drop = float('inf')
                for touch in touch_in_fall:
                    their_drop = do_drop(touch)
                    if their_drop < minimum_drop:
                        minimum_drop = their_drop
                if minimum_drop == 0:
                    on_ground.append(rect)
                    return my_falls

    while falling:
        faller = falling.pop()
        if touches_ground(on_ground, faller):
            on_ground.append(faller)
        else:
            fall_touching = list(get_down_touching(falling, faller))
            if not fall_touching:
                # move down, reappend
                falling.append(move_down(faller))
                falls += 1
            else:
                # pop those fall_touching and reprioritize
                for toucher in fall_touching:
                    falling.remove(toucher)
                falling.append(faller)
                for toucher in fall_touching:
                    falling.append(toucher)
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


def main():
    with open('input/day22_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    cube_pairs = [
        parse_cube_pair(line)
        for line in input_lines
    ]
    fallen, _ = fall_down(cube_pairs, verbose=True)
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
        unsafe_fall_rects = fallen.copy()
        unsafe_fall_rects.remove(the_rect)
        print(f'Disintegrating {the_rect}')
        _, unsafe_falls = fall_down(unsafe_fall_rects)
        print(f'Caused {unsafe_falls} falls')
        result += unsafe_falls
    print(f'Total: {result}')


if __name__ == '__main__':
    main()
