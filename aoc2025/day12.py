from typing import Tuple, Set, List, Optional

from attrs import define
from numpy import matmul
from scipy.optimize import linprog
from sortedcontainers import SortedList

from utils import add_coord, sub_coord, DIRECTIONS2


TEST_INPUT = '''0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
'''


def parse_shape(shape_str):
    _, _, real_shape = shape_str.partition(':\n')
    return {
        (i, j)
        for i, line in enumerate(real_shape.splitlines())
        for j, el in enumerate(line.strip())
        if el == '#'
    }


def parse_tile(tile_str):
    size_raw, _, shape_usage_raw = tile_str.partition(': ')
    size_x_raw, _, size_y_raw = size_raw.partition('x')
    return (int(size_x_raw), int(size_y_raw)), list(map(int, shape_usage_raw.split(' ')))


def parse_input(input_str):
    pieces = input_str.split('\n\n')
    shape_pieces = pieces[:-1]
    tile_piece = pieces[-1]
    shapes = [parse_shape(shape_piece) for shape_piece in shape_pieces]
    tiles = [parse_tile(tile_str) for tile_str in tile_piece.splitlines()]
    return shapes, tiles


def get_slack(shapes, tile):
    (size_x, size_y), shape_amount = tile
    return (size_x * size_y) - sum((len(shape) * amt for shape, amt in zip(shapes, shape_amount)))


def is_strictly_smaller(tile1, tile2):
    (x1, y1), shapes1 = tile1
    (x2, y2), shapes2 = tile2
    if x1 > x2 or y1 > y2:
        return False
    return all((amt1 >= amt2 for amt1, amt2 in zip(shapes1, shapes2)))


def min_tile(tile1, tile2):
    (x1, y1), shapes1 = tile1
    (x2, y2), shapes2 = tile2
    return (min(x1, x2), min(y1, y2)), list(map(min, zip(shapes1, shapes2)))


def rotate_around_center(to_rotate):
    # (0, -1) -> (1, 0)
    # (1, 0) -> (0, 1)
    # (0, 1) -> (-1, 0)
    # (-1, 0) -> (0, -1)
    x, y = to_rotate
    return -y, x


def rotate_around(to_rotate, center):
    return add_coord(rotate_around_center(sub_coord(to_rotate, center)), center)


def rotate_tile(tile):
    return {
        rotate_around(c, (1, 1))
        for c in tile
    }


def flip_x_tile(tile):
    return {
        (2 - x, y)
        for x, y in tile
    }


def flip_y_tile(tile):
    return {
        (x, 2 - y)
        for x, y in tile
    }


def get_variants(tile):
    return list({
        frozenset(tile_perm) for tile_perm in
        [
            tile,
            rotate_tile(tile),
            rotate_tile(rotate_tile(tile)),
            rotate_tile(rotate_tile(rotate_tile(tile))),
            flip_x_tile(tile),
            flip_y_tile(tile),
            rotate_tile(flip_x_tile(tile)),
            rotate_tile(flip_y_tile(tile))
        ]
    })


def get_bounding_box(shape):
    i_min = min((i for i, _ in shape))
    i_max = max((i for i, _ in shape))
    j_min = min((j for _, j in shape))
    j_max = max((j for _, j in shape))
    return i_min, i_max, j_min, j_max


def shape_str(shape):
    if not shape:
        return ''
    i_min, i_max, j_min, j_max = get_bounding_box(shape)
    return '\n'.join((
        ''.join((
            '#' if (i, j) in shape else '.'
            for j in range(j_min, j_max + 1)
        ))
        for i in range(i_min, i_max + 1)
    ))


@define
class TilingRestriction:
    x_size: int
    y_size: int
    shape_amt: List[int]


@define
class TilingCandidate:
    tiled: Set[Tuple[int, int]]
    shape_amt: List[int]
    restriction: Optional[TilingRestriction]

    def get_bb(self):
        return get_bounding_box(self.tiled)

    def get_badness(self):
        # higher number for more bad
        i_min, i_max, j_min, j_max = self.get_bb()
        area = (j_max - j_min + 1) * (i_max - i_min + 1)
        # i.e. full rectangles have zero badness
        num_unfilled = area - len(self.tiled)
        return num_unfilled + 5 * sum((max_amt - cand_amt for cand_amt, max_amt in zip(self.shape_amt, self.restriction.shape_amt)))

    def fits_in_restriction(self):
        i_min, i_max, j_min, j_max = self.get_bb()
        return (j_max - j_min + 1) <= self.restriction.y_size and (i_max - i_min + 1) <= self.restriction.x_size

    def fits_in_shape_amt(self):
        return all((cand_amt <= max_amt for cand_amt, max_amt in zip(self.shape_amt, self.restriction.shape_amt)))

    def fits_in(self):
        return self.fits_in_restriction() and self.fits_in_shape_amt()

    def is_solution(self):
        return self.fits_in() and all((cand_amt == max_amt for cand_amt, max_amt in zip(self.shape_amt, self.restriction.shape_amt)))

    def should_attempt_adding_shape(self, idx):
        self.shape_amt[idx] += 1
        result = self.fits_in_shape_amt()
        self.shape_amt[idx] -= 1
        return result


@define
class ShapeVariant:
    tiled: Set[Tuple[int, int]]
    shape_idx: int


def grow_shape(tiling_cand: TilingCandidate, variants: List[ShapeVariant]) -> List[TilingCandidate]:
    i_min, i_max, j_min, j_max = tiling_cand.get_bb()
    result = []
    for variant in variants:
        if not tiling_cand.should_attempt_adding_shape(variant.shape_idx):
            continue
        # we only grow upward and right
        for x_offset in range(max(i_min, i_max - 3), i_max + 3):
            for y_offset in range(j_min, j_max + 3):
                offset_var = {add_coord(var_el, (x_offset, y_offset)) for var_el in variant.tiled}
                if any((var_el in tiling_cand.tiled for var_el in offset_var)):
                    # overlap
                    continue
                # check if moving in some direction produces overlap
                tightness = False
                for direction in DIRECTIONS2:
                    offset_var_one_off = (add_coord(var_el, direction) for var_el in offset_var)
                    if any((var_el in tiling_cand.tiled for var_el in offset_var_one_off)):
                        tightness = True
                        break
                if not tightness:
                    continue
                # found candidate
                amt_copy = list(tiling_cand.shape_amt)
                amt_copy[variant.shape_idx] += 1
                cand = TilingCandidate(
                    tiling_cand.tiled | offset_var,
                    amt_copy,
                    tiling_cand.restriction
                )
                if cand.fits_in_restriction():
                    result.append(cand)
    return result


def initial_candidate(variant: ShapeVariant, num_shapes, restr: TilingRestriction):
    initial_shape_amt = [0] * num_shapes
    initial_shape_amt[variant.shape_idx] += 1
    return TilingCandidate(
        set(variant.tiled),
        initial_shape_amt,
        restr
    )


def into_fill_vector(x, y, var: ShapeVariant, x_size, y_size):
    tiled_offset = {add_coord(tile, (x, y)) for tile in var.tiled}
    return [
        1 if (i, j) in tiled_offset else 0
        for i in range(x_size)
        for j in range(y_size)
    ]


def linprog_solve(x_size, y_size, shapes, shape_amt):
    variants = [
        ShapeVariant(variant, i)
        for i, shape in enumerate(shapes)
        for variant in get_variants(shape)
    ]
    sol_len = (x_size - 2) * (y_size - 2) * len(variants)
    c = [-1] * sol_len
    A_ub_trans = [
        into_fill_vector(x, y, var, x_size, y_size)
        for x in range(x_size - 2) for y in range(y_size - 2) for var in variants
    ]
    A_ub = [[A_ub_trans[j][i] for j in range(sol_len)] for i in range(x_size * y_size)]
    b_ub = [1] * x_size * y_size
    A_eq = [
        [
            1 if var.shape_idx == i else 0
            for x in range(x_size - 2) for y in range(y_size - 2) for var in variants
        ]
        for i, shape in enumerate(shapes)
    ]
    b_eq = shape_amt
    print(sol_len)
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, integrality=1)
    if result.status != 0:
        print(result)
        return None
    if not result.success:
        print(result)
    placements = result.x
    tiled_fill_vector_direct = matmul(A_ub, placements)
    tiled_fill_vector = list(map(round, tiled_fill_vector_direct))
    shape_amt_check = matmul(A_eq, placements)
    print(shape_amt_check, shape_amt, sum(tiled_fill_vector))
    print(sum(placements), sum(shape_amt))
    print(max(map(lambda pr: abs(pr[0] - pr[1]), zip(tiled_fill_vector, tiled_fill_vector_direct))))
    return TilingCandidate(
        {(i, j) for i in range(x_size) for j in range(y_size) if tiled_fill_vector[i * y_size + j] == 1},
        list(map(int, shape_amt_check)),
        TilingRestriction(
            x_size, y_size, shape_amt
        )
    )


@define
class TilingArea:
    to_tile: Set[Tuple[int, int]]
    x_bound: int
    y_bound: int

    def num_tiles(self) -> int:
        return len(self.to_tile)

    def get_lower_half(self) -> 'TilingArea':
        if self.x_bound > self.y_bound:
            # split along x_bound // 2
            return TilingArea(
                {t for t in self.to_tile if t[0] <= self.x_bound // 2},
                self.x_bound // 2,
                self.y_bound,
            )
        else:
            # split along y_bound // 2
            return TilingArea(
                {t for t in self.to_tile if t[1] <= self.y_bound // 2},
                self.x_bound,
                self.y_bound // 2,
            )

    def subtract_lower_subset(self, subset: 'TilingArea') -> Tuple['TilingArea', Tuple[int, int]]:
        def connected_to_upper(t):
            x, y = t
            if self.x_bound > self.y_bound:
                # usually x > self.x_bound // 2. But we allow 2 overextensions
                return x + 2 > self.x_bound // 2
            else:
                # usually y > self.y_bound // 2. But we allow 2 overextensions
                return y + 2 > self.x_bound // 2
        rem_to_tile = {
            t
            for t in self.to_tile
            if (t not in subset.to_tile) and connected_to_upper(t)
        }
        min_x = min((t[0] for t in rem_to_tile))
        max_x = max((t[0] for t in rem_to_tile))
        min_y = min((t[1] for t in rem_to_tile))
        max_y = max((t[1] for t in rem_to_tile))
        return TilingArea(
            {sub_coord(t, (min_x, min_y)) for t in rem_to_tile},
            max_x - min_x,
            max_y - min_y,
        ), (min_x, min_y)


def get_square_area(x_size, y_size) -> TilingArea:
    return TilingArea(
        {(i, j) for i in range(x_size) for j in range(y_size)},
        x_size,
        y_size,
    )


def into_fill_vector_area(x, y, var: ShapeVariant, area: TilingArea):
    tiled_offset = {add_coord(tile, (x, y)) for tile in var.tiled}
    return [
        1 if (i, j) in tiled_offset else 0
        for (i, j) in area.to_tile
    ]


LINPROG_TILE_BOUND = 80


def transpose(two_d_array):
    return [[two_d_array[j][i] for j in range(len(two_d_array))] for i in range(len(two_d_array[0]))]


def solve_tiling_by_linprog(area: TilingArea, shapes, shape_amt):
    variants = [
        ShapeVariant(variant, i)
        for i, shape in enumerate(shapes)
        for variant in get_variants(shape)
    ]
    sol_places = [
        (x, y, i)
        for (x, y) in area.to_tile
        for i, variant in enumerate(variants)
        if {add_coord(t, (x, y)) for t in variant.tiled}.issubset(area.to_tile)
    ]
    sol_len = len(sol_places)
    print(sol_len, shape_amt)
    if len(sol_places) == 0:
        # there is no legal place for any tiles
        return TilingCandidate(set(), [0] * len(shape_amt), None)
    # as many pieces as possible
    c = [-1] * sol_len
    # weigh piece importance by shape_amt
    c_shape_importance = -1 * matmul(shape_amt, [
        [1 if variants[var_idx].shape_idx == i else 0 for x, y, var_idx in sol_places]
        for i in range(len(shapes))
    ])
    # maximize number of filled tiles
    c_fill_tiles = matmul([-1] * area.num_tiles(), transpose([
        into_fill_vector_area(x, y, variants[var_idx], area)
        for x, y, var_idx in sol_places
    ]))
    # weigh these about 2:1. note that we have to scale the tile filling
    c = c_shape_importance * 2 + c_fill_tiles * (sum(shape_amt) // len(shape_amt))
    A_ub_trans = [
        into_fill_vector_area(x, y, variants[var_idx], area) + [
            1 if variants[var_idx].shape_idx == i else 0
            for i, shape in enumerate(shapes)
        ]
        for x, y, var_idx in sol_places
    ]  # sol_len X (area.num_tiles() + len(shapes))
    A_ub = [[A_ub_trans[j][i] for j in range(sol_len)] for i in range(area.num_tiles() + len(shapes))]
    # (area.num_tiles() + len(shapes)) X sol_len
    b_ub = ([1] * area.num_tiles()) + shape_amt
    # print(sol_len)
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, integrality=1)
    if result.status != 0:
        print(result)
        return None
    if not result.success:
        print(result)
    placements = result.x
    total_result = matmul(A_ub, placements)
    tiled_fill_vector_direct = total_result[:area.num_tiles()]
    tiled_fill_vector = list(map(round, tiled_fill_vector_direct))
    shape_amt_check = total_result[area.num_tiles():]
    # print(sum(tiled_fill_vector))
    # print(sum(placements), sum(shape_amt))
    # print(max(map(lambda pr: abs(pr[0] - pr[1]), zip(tiled_fill_vector, tiled_fill_vector_direct))))
    return TilingCandidate(
        {t for t, v_el in zip(area.to_tile, tiled_fill_vector) if v_el == 1},
        list(map(round, shape_amt_check)),
        None
    )


def check_can_tile(x_size, y_size, shapes, shape_amt):
    near_optimum_tiling = solve_by_repeated_halving(get_square_area(x_size, y_size), shapes, shape_amt)
    if all((w == o for w, o in zip(shape_amt, near_optimum_tiling.shape_amt))):
        return near_optimum_tiling
    else:
        print(f'Failed to fit {shape_amt} in {x_size} X {y_size}: only got {near_optimum_tiling.shape_amt}')
        print(shape_str(near_optimum_tiling.tiled))
        return None


def solve_by_repeated_halving(area: TilingArea, shapes, shape_amt):
    if all((s == 0 for s in shape_amt)):
        return TilingCandidate(
            set(), shape_amt, None
        )
    if area.num_tiles() <= LINPROG_TILE_BOUND:
        return solve_tiling_by_linprog(area, shapes, shape_amt)
    lower = area.get_lower_half()
    # put as many shapes as you can into lower_sol
    lower_sol = solve_by_repeated_halving(lower, shapes, shape_amt)
    if lower_sol is None:
        print(f'Fitting {shape_amt} into subset of {area.x_bound} X {area.y_bound} seems unfeasible')
        return None
    lower_subset = TilingArea(lower_sol.tiled, lower.x_bound, lower.y_bound)
    # NOTE: we could flip lower_subset if the number of unfilled tiles on the
    # upside is lower than the number of unfilled tiles on the bottom side
    # rest must go into remaining_upper
    remaining_upper, offset = area.subtract_lower_subset(lower_subset)
    remaining_shapes = [si - sl for si, sl in zip(shape_amt, lower_sol.shape_amt)]
    # print(len(lower_sol.tiled), lower_sol.shape_amt, remaining_shapes)
    # print(shape_str(lower_sol.tiled))

    upper_sol = solve_by_repeated_halving(remaining_upper, shapes, remaining_shapes)
    if upper_sol is None:
        print(f'Fitting {remaining_shapes} into subset of {remaining_upper.x_bound} X {remaining_upper.y_bound} seems unfeasible')
        return None
    # print(len(upper_sol.tiled), upper_sol.shape_amt)
    # print(shape_str(upper_sol.tiled))

    combined_sol = TilingCandidate(
        lower_sol.tiled | {add_coord(t, offset) for t in upper_sol.tiled},
        list(map(sum, zip(lower_sol.shape_amt, upper_sol.shape_amt))),
        None
    )
    assert(len(combined_sol.tiled) == len(lower_sol.tiled) + len(upper_sol.tiled))
    # print(len(combined_sol.tiled), combined_sol.shape_amt)
    # print(shape_str(combined_sol.tiled))
    return combined_sol


def linprog_find_largest(x_size, y_size, shapes, shape_amt):
    variants = [
        ShapeVariant(variant, i)
        for i, shape in enumerate(shapes)
        for variant in get_variants(shape)
    ]
    sol_len = (x_size - 2) * (y_size - 2) * len(variants)
    c = [-1] * sol_len
    A_ub_trans = [
        into_fill_vector(x, y, var, x_size, y_size) + [
            -1 if var.shape_idx == i else 0
            for i, shape in enumerate(shapes)
        ]
        for x in range(x_size - 2) for y in range(y_size - 2) for var in variants
    ]  # sol_len X (x_size * y_size + len(shapes))
    A_ub = [[A_ub_trans[j][i] for j in range(sol_len)] for i in range(x_size * y_size + len(shapes))]
    # (x_size * y_size + len(shapes)) X sol_len
    b_ub = ([1] * x_size * y_size) + ([s * -1 for s in shape_amt])
    # print(sol_len)
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, integrality=1)
    if result.status != 0:
        print(result)
        return None
    if not result.success:
        print(result)
    placements = result.x
    total_result = matmul(A_ub, placements)
    tiled_fill_vector_direct = total_result[:x_size * y_size]
    tiled_fill_vector = list(map(round, tiled_fill_vector_direct))
    shape_amt_check = total_result[x_size * y_size:]
    print(sum(tiled_fill_vector))
    print(sum(placements), sum(shape_amt))
    print(max(map(lambda pr: abs(pr[0] - pr[1]), zip(tiled_fill_vector, tiled_fill_vector_direct))))
    return TilingCandidate(
        {(i, j) for i in range(x_size) for j in range(y_size) if tiled_fill_vector[i * y_size + j] == 1},
        list(map(int, shape_amt_check)),
        TilingRestriction(
            x_size, y_size, shape_amt
        )
    )


def genetic_shape_grower(x_size, y_size, shapes, shape_amt):
    variants = [
        ShapeVariant(variant, i)
        for i, shape in enumerate(shapes)
        for variant in get_variants(shape)
    ]
    restr = TilingRestriction(x_size, y_size, shape_amt)
    first_shape_idx = next((i for i, amt in enumerate(shape_amt) if amt != 0))
    candidates = SortedList([
        initial_candidate(var, len(shapes), restr)
        for var in variants
        if var.shape_idx == first_shape_idx
    ], key=lambda c: c.get_badness())
    iteration = 0
    while candidates:
        cand = candidates.pop(0)
        # print(f'=====: {iteration}, {cand.get_badness()}, {len(cand.tiled)}, {cand.shape_amt}')
        # print(shape_str(cand.tiled))
        new_cands = grow_shape(cand, variants)
        for new_cand in new_cands:
            if new_cand.is_solution():
                return new_cand
            else:
                candidates.add(new_cand)
        iteration += 1
    return None


def push_shapes(x_size, y_size, shapes, shape_amt):
    shape_idx_to_increase = 0
    cur_shape_amt = list(shape_amt)
    while shape_idx_to_increase < len(shapes):
        print(cur_shape_amt)
        sol = linprog_solve(x_size, y_size, shapes, cur_shape_amt)
        while sol is not None:
            print(shape_str(sol.tiled))
            last_valid_amt = cur_shape_amt[shape_idx_to_increase]
            cur_shape_amt[shape_idx_to_increase] = last_valid_amt + 1
            sol = linprog_solve(x_size, y_size, shapes, cur_shape_amt)
        cur_shape_amt[shape_idx_to_increase] = last_valid_amt
        shape_idx_to_increase += 1
    return cur_shape_amt


def fits_without_squeezing(x_size, y_size, shape_amt):
    num_3_by_3_tiles = (x_size // 3) * (y_size // 3)
    return sum(shape_amt) <= num_3_by_3_tiles


# got this from https://github.com/StevenBtw/AoC_2025/tree/main/day12/betterinput
# via reddit. But my solution finds correct tilings that are deemed impossible (for unknown reason) by that URL

TEST_INPUT_HARD = '''0:
##
##
##

1:
###
###

2:
##
##
.#

3:
.#.
###
.#.

4:
###
#..
###

5:
#.#
###
#.#

44x47: 55 55 55 27 27 28
45x49: 36 36 36 36 146 36
40x39: 43 42 42 21 21 21
37x38: 53 53 35 17 17 18
45x50: 69 70 70 34 34 35
50x46: 92 92 61 30 30 30
39x40: 19 20 20 59 60 60
'''


def main():
    shapes, tiles = parse_input(TEST_INPUT_HARD)
    # with open('input/day12.txt') as f:
    #     shapes, tiles = parse_input(f.read())

    possible_tiles = {i: tile for i, tile in enumerate(tiles) if get_slack(shapes, tile) >= 0}
    for i, tile in possible_tiles.items():
        print(i, get_slack(shapes, tile))

    print(f'Awkward guess: {len(possible_tiles)}')

    # this one fits!
    # possible_tiles[-1] = (35, 35), [66, 28, 14, 22, 22, 20]

    result = 0

    for i, tile in sorted(possible_tiles.items(), key=lambda pr:
        pr[0]
        #(pr[1][0][0] - 2) * (pr[1][0][1] - 2)
    ):
        (x_size, y_size), shape_amt = tile
        if fits_without_squeezing(x_size, y_size, shape_amt):
            result += 1
            continue
        # ugh, all examples in day12.txt are easy, i.e. fit without squeezing. lame
        print(f'Need to squeeze {shape_amt} in {x_size} X {y_size}')
        # solution = linprog_solve(x_size, y_size, shapes, shape_amt)
        # shape_amt = [46, 28, 14, 21, 22, 20]
        # print(x_size, y_size)
        # solution = linprog_find_largest(x_size, y_size, shapes, shape_amt)
        print(x_size, y_size, shape_amt)
        solution = check_can_tile(x_size, y_size, shapes, shape_amt)
        # print(best_shape)
        # solution = genetic_shape_grower(x_size, y_size, shapes, shape_amt)
        if solution is not None:
            result += 1
            print(f'{i}: =*=*=*=*')
            print(shape_str(solution.tiled))
        # print('\n')

    print(f'Better guess: {result}')


'''   
40 * 40 * 28 (= len(variants)) = 44800 (length of x)

5 * 8 * 28 = 1120 (probably doable)

Aub * x <= [all ones]
Aeq * x = target
x <= [all ones]

'''


'''
[67. 28. 14. 21. 22. 20.] [67, 28, 14, 21, 22, 20] 1143
171.9999999999999 172
8.948397578478762e-14
########.###.###.###.##########.###
######.################.########.#.
###################################
##############.#########.########.#
################.##############.###
###.##########.####################
####################.#############.
############.#.##########.####.####
#######.#########.#######.#########
#########.####.####################
.########.#########################
##############.####.###############
###################################
################.##############.##.
#############.#####################
############.####.###.####.########
##########.###.#########...########
.#########.############..##########
.########.#####################.###
.####.######################.######
#.#.#######.#.###############..####
########.###############..#########
#.################.###.############
.##################.###############
.##################################
###################################
###################################
####.#############################.
###################################
###################################
###.###############################
#####.#############################
###################################
.#########.#########.##############
###.####.####.###.######.#########.
'''


if __name__ == '__main__':
    main()
