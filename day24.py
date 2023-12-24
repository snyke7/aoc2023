import numpy as np


TEST = '''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''


def parse_tuple(the_str: str):
    return np.array(tuple(map(int, the_str.split(', '))))


def parse_vector(line):
    left, _, right = line.strip().partition(' @ ')
    return parse_tuple(left), parse_tuple(right)


def get_intersect_times(vec1, vec2, truncate_z=True):
    pos1, vel1 = vec1
    pos2, vel2 = vec2
    if truncate_z:
        pos1 = pos1[:2]
        pos2 = pos2[:2]
        vel1 = vel1[:2]
        vel2 = vel2[:2]
    # solve: pos1 + vel1 * t1 = pos2 + vel2 * t2
    # equivalently: vel1 * t1 - vel2 * t2 = pos2 - pos1
    # [vel1 vel2] · [t1; -t2] = pos2 - pos1
    a = np.transpose(
            np.array([vel1, vel2])
        )
    b = pos2 - pos1
    t1, neg_t2 = np.linalg.solve(a, b)
    return t1, -neg_t2


def get_future_intersect_place(vec1, vec2, truncate_z=True):
    try:
        t1, t2 = get_intersect_times(vec1, vec2, truncate_z=truncate_z)
    except np.linalg.LinAlgError:
        return None
    if t1 < 0 or t2 < 0:  # intersected in the past
        return None
    return vec1[0] + vec1[1] * t1


def future_intersect_within_bound(vec1, vec2, bounds, truncate_z=True):
    intersect = get_future_intersect_place(vec1, vec2, truncate_z=truncate_z)
    if intersect is None:
        return False
    return bounds[0] <= intersect[0] <= bounds[1] and bounds[0] <= intersect[1] <= bounds[1]


def count_colliding(vectors, bounds, truncate_z=True):
    count = 0
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            if future_intersect_within_bound(vectors[i], vectors[j], bounds, truncate_z=truncate_z):
                count += 1
    return count


def main():
    with open('input/day24_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    vectors = [parse_vector(line) for line in input_lines]
    intersect_bounds = 200000000000000, 400000000000000
    intersect_bounds2 = 7, 27
    print(count_colliding(vectors, intersect_bounds))


if __name__ == '__main__':
    main()
