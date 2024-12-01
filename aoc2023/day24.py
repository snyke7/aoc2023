import numpy as np
from collections import defaultdict
from itertools import product


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
            # if np.any(vectors[i][1] == vectors[j][1]):
            #     print(f'Some overlap: {i} {j}')
    return count


primes = []
sieved_until = None


def extend_primes():
    # more primes were requested, start sieving
    sieve = defaultdict(lambda: True)
    global sieved_until
    if sieved_until is None:
        prev_sieved = 2
        sieved_until = 1000000
    else:
        prev_sieved = sieved_until
        sieved_until *= 2
    print(f'Sieving until {sieved_until}')
    for prime in primes:
        for n in range(prev_sieved // prime, sieved_until // prime + 1):
            sieve[prime * n] = False
    for n in range(prev_sieved, sieved_until):
        if sieve[n]:
            primes.append(n)
            for m in range(prev_sieved // n, sieved_until // n + 1):
                sieve[n * m] = False


def prime_gen():
    yield from primes
    extend_primes()
    yield from prime_gen()


def get_prime_divisors_and_powers(num):
    if num == 1:
        return []
    for prime in prime_gen():
        if num % prime == 0:
            power = 0
            while num % prime == 0:
                num = num // prime
                power += 1
            return [(prime, power)] + get_prime_divisors_and_powers(num)
        if prime ** 2 > num:
            return [(num, 1)]


def get_divisors(num):
    if num == 0:
        return []
    if num == 1:
        return [1]
    prime_power_divisors = get_prime_divisors_and_powers(num)
    prime_divisors = [prime for prime, _ in prime_power_divisors]
    power_tups = product(*(range(power + 1) for _, power in prime_power_divisors))
    result = []
    for power_tup in power_tups:
        this = 1
        for prime, power in zip(prime_divisors, power_tup):
            this *= prime ** power
        result.append(this)
    return sorted(result)


def main():
    with open('input/day24_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    vectors = [parse_vector(line) for line in input_lines]
    intersect_bounds = 200000000000000, 400000000000000
    intersect_bounds2 = 7, 27
    print(count_colliding(vectors, intersect_bounds))
    # for part2, find ps, vs so that
    # p1 + v1 * t1 = ps + vs * t1
    # p2 + v2 * t2 = ps + vs * t2
    # p3 + v3 * t3 = ps + vs * t3
    # ....
    # note that unknowns are: all ts, ps, and vs
    # subtract p1 + v1 * t1 from all equations:
    # p2 + v2 * t2 - sub = vs * (t2 - t1)
    # p3 + v3 * t3 - sub = vs * (t3 - t1)
    # p4 + v4 * t4 - sub = vs * (t4 - t1)
    # ...
    # this is not linear! -> diophantine..?

    # p1[0] + v1[0] * t1 = ps[0] + vs[0] * t1
    # p1[0] + v1[0] * u_t1 = u_ps0 + u_vs0 * u_t1 <- 3 unknowns
    # p1[1] + v1[1] * u_t1 = u_ps1 + u_vs1 * u_t1
    # p1[2] + v1[2] * u_t1 = u_ps2 + u_vs2 * u_t1
    #
    # p1 = ps + (vs - v1) * t1
    # p2 = ps + (vs - v2) * t2
    # p3 = ps + (vs - v3) * t3
    # ..
    # p2 = (p1 - (vs - v1) * t1) + (vs - v2) * t2
    # p3 = (p1 - (vs - v1) * t1) + (vs - v3) * t3
    # p3 - p2 = (vs - v3) * t3 - (vs - v2) * t2
    # p2 - p1 = (vs - v2) * t2 - (vs - v1) * t1
    # p2 - p1 = (vs - v1 + (v1 - v2)) * t2 - (vs - v1) * t1

    # p2 - p1 = vs' * (t2 - t1) + (v1 - v2) * t2  <- 3 equations, 5 unknowns (t2, t1, 3vs')
    # p3 - p1 = vs' * (t3 - t1) + (v1 - v3) * t3  <- 3 equations, 5 unknowns (t3, t1, 3vs')
    # together: 6 equations, 6 unknowns

    # F1 = x1 * (y - z) + C1 * y
    # F2 = x2 * (y - z) + C2 * y
    # F3 = x3 * (y - z) + C3 * y
    # G1 = x1 * (u - z) + D1 * u
    # G2 = x2 * (u - z) + D2 * u
    # G3 = x3 * (u - z) + D3 * u
    # ah wait but one of the coordinates will overlap, right
    # so we can find
    # (pi - pj)[k] = vs' * (ti - tj)
    base_triples = [
        (i, j, next((k for k in range(3) if vectors[i][1][k] == vectors[j][1][k])))
        for i in range(len(vectors))
        for j in range(i + 1, len(vectors)) if
        np.any((vectors[i][1] == vectors[j][1]))
    ]
    print(len(base_triples))
    easy_coord_map = {}
    for i, j, k in base_triples:
        if abs(vectors[i][0][k] - vectors[j][0][k]) == 0:
            print(f'Found zero! {i, vectors[i][0]} {j, vectors[j][0]} {k}')
            print(f'So we must have vs[{k}] = {vectors[i][1][k]} = {vectors[j][1][k]}..?')
            continue
        divs = get_divisors(abs(vectors[i][0][k] - vectors[j][0][k]))
        if k not in easy_coord_map or len(easy_coord_map[k][2]) > len(divs):
            easy_coord_map[k] = (i, j, [-1 * div for div in divs[::-1]] + divs)
    print(easy_coord_map)
    for v0d in easy_coord_map[0][2]:
        v0 = v0d + vectors[easy_coord_map[0][0]][1][0]
        for v1d in easy_coord_map[1][2]:
            v1 = v1d + vectors[easy_coord_map[1][0]][1][1]
            for v2d in easy_coord_map[2][2]:
                v2 = v2d + vectors[easy_coord_map[2][0]][1][2]
                # (pi - pj)[k] = vs' * (ti - tj)
                # ti - tj = (pi - pj)[k] / vs'[k]
                i = easy_coord_map[0][0]
                j = easy_coord_map[0][1]
                pdiff = vectors[i][0][0] - vectors[j][0][0]
                t0d = pdiff // v0d
                # pi + vi * ti = ps + vs * ti
                # pj + vj * tj = ps + vs * tj
                # pi = ps + (vs - vi) * ti
                # pj = ps + (vs - vj) * tj
                # pi - pj = (vs - vi) * ti - (vs - vj) * tj
                # pi - pj = (vs - vi) * (tdiff + tj) - (vs - vj) * tj
                # pi - pj = (vs - vi) * tdiff + (vs - vi) * tj - (vs - vj) * tj
                # pi - pj - (vs - vi) * tdiff = tj * ((vs - vi) - (vs - vj))
                # print(t0d * v0d - pdiff)
                vs = [v0, v1, v2]
                lhs = vectors[i][0][1] - vectors[j][0][1] - (vs[1] - vectors[i][1][1]) * t0d
                rhs = (vs[1] - vectors[i][1][1]) - (vs[1] - vectors[j][1][1])
                if lhs % rhs != 0:
                    continue
                tj = lhs // rhs
                ti = t0d + tj
                pos2diff = vectors[i][0][2] - vectors[j][0][2] - (
                    (vs[2] - vectors[i][1][2]) * ti - (vs[2] - vectors[j][1][2]) * tj
                )
                if pos2diff != 0:
                    continue
                # pi + vi * ti = ps + vs * ti
                # ps = pi + vi * ti - vs * ti
                ps = [
                    vectors[i][0][0] + vectors[i][1][0] * ti - vs[0] * ti,
                    vectors[i][0][1] + vectors[i][1][1] * ti - vs[1] * ti,
                    vectors[i][0][2] + vectors[i][1][2] * ti - vs[2] * ti,
                ]
                is_bad = False
                for k in range(len(vectors)):
                    pk = vectors[k][0]
                    vk = vectors[k][1]
                    for c in range(3):
                        if (pk[c] - ps[c]) % (vs[c] - vk[c]) != 0:
                            is_bad = True
                if is_bad:
                    continue
                # print(lhs, rhs, lhs % rhs, t0d, v0d, pdiff, i, j, tj, pos2diff, ti, vs, ps, sum(ps))
                print(sum(ps))
                # pk + vk * tk = ps + vs * tk
                # pk - ps = (vs - vk) * tk
                # print(max(abs(
                #     np.array(ps) + np.array(vs) * ti -
                #     (vectors[i][0] + vectors[i][1] * ti)
                # )))
                # print(max(abs(
                #     np.array(ps) + np.array(vs) * tj -
                #     (vectors[j][0] + vectors[j][1] * tj)
                # )))

    # pi + vi * ti = ps + vs * ti
    # pj + vj * tj = ps + vs * tj -->
    # pi = ps + (vs - vi) * ti
    # pj = ps + (vs - vj) * tj
    # pi - pj = (vs - vi) * ti - (vs - vj) * tj
    # (pi - pj)[k] = (vs - vi[k]) * ti - (vs - vj[k]) * tj
    # (pi - pj)[k] = (vs - vc) * ti - (vs - vc) * tj
    # (pi - pj)[k] = (vs - vc) * (ti - tj)
    # vs[k] = divisor + vc
    # if (pi - pj)[k] = 0, and we know (ti - tj ≠ 0), then we must have vs[k] = vc


if __name__ == '__main__':
    main()
