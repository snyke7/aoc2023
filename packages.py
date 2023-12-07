from math import floor

# for: https://aoc.infi.nl/2023?mtm_campaign=aoc2023&mtm_source=aoc


CORNERS = [
    [(52, 4), (-85, -84), (-16, 71), (13, 88), (-9, 30), (-66, -23)],
    [(-32, -14), (6, 92), (-33, 9)],
    [(-36, -74), (-90, 56), (77, 76), (-65, -59), (65, -24)],
    [(-49, -55), (76, -4), (-81, -20), (78, -2), (-51, 42)],
    [(-47, -22), (15, 94), (47, 6), (44, 88), (-68, 1), (-6, 92)],
    [(25, -7), (-41, -61), (7, 36), (-28, -78)],
    [(-86, 83), (-68, -46), (71, -33)],
    [(-86, 69), (-40, 57), (18, 73)],
    [(-60, 82), (-72, 28), (-4, 77), (-56, -86), (57, -47), (18, 71)],
    [(-80, 39), (90, 13), (-31, 23), (-61, -37), (32, 62), (-7, 34)],
    [(62, -82), (31, -67), (-66, 39), (52, 61)],
    [(-44, -21), (-93, 76), (-55, 69)],
    [(-74, 78), (35, -100), (42, -95)],
    [(78, 46), (-13, 95), (34, -32), (8, -81)],
    [(94, -82), (-86, -74), (-17, 23), (-82, 79), (-82, 63), (-99, -18)],
    [(5, -8), (-23, -31), (-37, 5), (84, 58), (33, 35)],
    [(43, 52), (-13, 47), (43, -82), (-7, 10), (-63, 43), (-87, 58)],
    [(42, 16), (3, 59), (56, 82)],
    [(-97, 92), (-33, -59), (94, 18), (-36, -96), (-98, -65), (77, -40), (-17, -43)],
    [(30, -64), (-29, -65), (-100, -31), (-9, -55), (67, -8)],
    [(-55, 26), (46, -98), (-76, -99), (51, 56), (53, 51), (-15, -55)],
    [(-75, 53), (-12, 7), (-99, 66), (52, -25), (73, -41), (86, -33)],
    [(20, 82), (9, 12), (46, 0), (48, -40), (-28, 38)],
    [(99, -90), (75, 9), (26, 4), (32, -55)],
    [(19, -91), (-54, 80), (83, -56), (-100, 39), (-41, -28), (-34, 60), (35, 36)],
]


def part1():
    return floor(sum((
        max(((x ** 2 + y ** 2) ** 0.5 for x, y in package))
        for package in CORNERS
    )))


def get_dist(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def get_longest_vertex_idx(package):
    max_dist = float('-inf')
    indices = -1, -1
    for i in range(len(package)):
        for j in range(i + 1, len(package)):
            dist = get_dist(package[i], package[j])
            if dist > max_dist:
                max_dist = dist
                indices = i, j
    return indices


def get_optimal_center_and_radius(package):
    i, j = get_longest_vertex_idx(package)
    p1 = package[i]
    p2 = package[j]
    bc = (p2[0] + p1[0]) / 2.0, (p2[1] + p1[1]) / 2.0
    radius1 = get_dist(p1, p2) / 2.0
    outside_points = [p for p in package if get_dist(p, bc) > radius1]
    if not outside_points:
        return bc, radius1
    # otherwise, calculate intersections of perpendicular bisectors
    # equation: (p2 + p1)/ 2 + t * rot90(p2 - p1) = (p3 + p1) /2 + s * rot90(p3 - p1)
    # t * Mrot90 · d1 - s * Mrot90 · d2 = c2 - c1
    # [Mrot90 · d1  |  -Mrot90 · d2] · [t; s] = c2 - c1
    # Mrot90 = [0 -1; 1 0]
    # t = ((c2 - c1)[0] - s*d2[0]) / d1[0]
    # t*d1[1] - s * d2[1] = (c2 - c1)[1]
    # ((c2 - c1)[0] + s*d2[0]) / d1[0] * d1[1] - s * d2[1] = (c2 - c1)[1]
    # s * (-d2[1] + d2[0] / d1[0] * d1[1]) + (c2 - c1)[0] / d1[0] * d1[1] = (c2 - c1)[1]
    # s = ((c2 - c1)[1] - (c2 - c1)[0] / d1[0] * d1[1]) / (-d2[1] + d2[0] / d1[0] * d1[1])
    #
    # probably cleaner to import numpy.. oh well
    d1 = (p1[1] - p2[1]), (p2[0] - p1[0])
    max_t = 0
    max_t_causer = None
    for p in outside_points:
        bc2 = (p[0] + p1[0]) / 2.0, (p[1] + p1[1]) / 2.0
        d2 = (p1[1] - p[1]), (p[0] - p1[0])
        dc = bc2[0] - bc[0], bc2[1] - bc[1]
        s = (dc[1] - (dc[0] / d1[0] * d1[1])) / (-d2[1] + (d2[0] / d1[0] * d1[1]))
        t = (dc[0] + s * d2[0]) / d1[0]
        if abs(t) > abs(max_t):
            max_t = t
            max_t_causer = p
    center = (bc[0] + max_t * d1[0]), (bc[1] + max_t * d1[1])
    radius = get_dist(center, p1)
    # check that this center, radius is actually correct,
    # since the points of the longest vertex do not necessarily lie on the circle!
    for p in package:
        if get_dist(p, center) - radius > 0.001:
            print(p, package, center, radius, p1, p2, p in outside_points, get_dist(p, center))
            print('detected corner case')
            # p and max_t_causer must be on the same side. we should get the right circle
            # after removing the point which is closest to p and max_t_causer
            changed_package = list(package)
            if get_dist(p1, p) + get_dist(p1, max_t_causer) < \
                    get_dist(p2, p) + get_dist(p2, max_t_causer):
                to_remove = p1
            else:
                to_remove = p2
            changed_package.remove(to_remove)
            center, radius = get_optimal_center_and_radius(changed_package)
            assert get_dist(p1, center) - radius < 0.001
            print(p, package, center, radius, p1, p2, p in outside_points, get_dist(to_remove, center))
            return center, radius
    return center, radius


def part2():
    test_package1 = [(-1, 0), (1, 4), (1, -4)]
    test_package2 = [(0, 4), (3, -2), (-1, -2), (-2, 0)]
    test_package3 = [(-4, 0), (1, 4), (1, -4)]
    print(get_optimal_center_and_radius(test_package1))
    print(get_optimal_center_and_radius(test_package2))
    print(get_optimal_center_and_radius(test_package3))
    print(floor(sum((get_optimal_center_and_radius(p)[1] for p in CORNERS))))


def main():
    print(part1())
    part2()


if __name__ == '__main__':
    main()
