from functools import reduce
from math import factorial, gcd
import scipy as sp
from typing import TypeVar, Callable, List, Dict, Tuple

from utils import dijkstra_steps, add_coord, sub_coord


TEST_INPUT = '''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''


def parse_lights(light_str):
    return tuple((1 if el == '#' else 0 for el in light_str[1:-1])), len(light_str) - 2


def parse_buttons(buttons_str, dimension):
    return [
        tuple((1 if i in set(map(int, button_str[1:-1].split(','))) else 0 for i in range(dimension)))
        for button_str in buttons_str
    ]


def parse_joltage(joltage_str):
    return tuple(map(int, joltage_str[1:-1].split(',')))


def parse_line(input_line):
    parts = input_line.split(' ')
    lights, dimension = parse_lights(parts[0])
    return lights, parse_buttons(parts[1:-1], dimension), dimension, parse_joltage(parts[-1])


def parse_input(input_str):
    return list(map(parse_line, input_str.splitlines()))


def everywhere_in_dimension(dimension):
    if dimension == 0:
        yield tuple()
    else:
        for el in everywhere_in_dimension(dimension - 1):
            yield 0, *el
            yield 1, *el


def add_button(loc, button):
    return tuple(((l + b) % 2 for l,b in zip(loc, button)))


def into_graph(buttons, dimension):
    return {
        loc: [
            add_button(loc, button)
            for button in buttons
        ]
        for loc in everywhere_in_dimension(dimension)
    }


def compute_pt1(parsed_inputs):
    result = 0
    for lights, buttons, dimension, _ in parsed_inputs:
        graph = into_graph(buttons, dimension)
        presses = dijkstra_steps(graph, next(everywhere_in_dimension(dimension)))
        result += presses[lights]
    return result


A = TypeVar('A')


def dyn_dijkstra_to(graph: Callable[[A, int], List[Tuple[A, int]]], start: A, discard: Callable[[A], bool], end: A) -> int:
    result = {start: 0}
    new = [(start, 0)]
    while new:
        node, node_idx = new.pop(0)
        cost = result[node]
        if end in result and cost >= result[end]:
            continue
        for neigbor, call_idx in graph(node, node_idx):
            if discard(neigbor):
                continue
            if neigbor not in result or result[neigbor] > cost + 1:
                result[neigbor] = cost + 1
                new.append((neigbor, call_idx))
    return result[end]


def direct_solve_dijkstra(buttons, dimensions, joltage):
    return dyn_dijkstra_to(
        lambda a, idx: [
            (add_coord(a, button), i + idx)
            for i, button in enumerate(buttons[idx:])
        ],
        (0,) * dimensions,
        lambda a: any((el < 0 for el in sub_coord(joltage, a))),
        joltage
    )

def mul_coord(coord: Tuple[int, ...], m: int):
    return tuple((m * c for c in coord))


def direct_dynamic(buttons, dimensions, rem_joltage):
    if all((c == 0 for c in rem_joltage)):
        return 0
    if not buttons:
        # but joltage remaining: no solution
        return float('inf')
    if any((c < 0 for c in rem_joltage)):
        return float('inf')
    max_first_button_use = min((j for j, c in zip(rem_joltage, buttons[0]) if c == 1))
    return min((
        direct_dynamic(buttons[1:], dimensions, sub_coord(rem_joltage, mul_coord(buttons[0], j))) + j
        for j in range(max_first_button_use + 1)
    ))


def get_sums_to(the_sum, numbers, check_prefix: Callable[[Tuple[int, ...]], bool]):
    if numbers == 0:
        if the_sum != 0:
            raise ValueError(f"Cannot sum to {the_sum} with no numbers")
        else:
            yield tuple()
    elif numbers == 1:
        yield (the_sum, )
    else:
        for i in reversed(range(the_sum + 1)):
            if not check_prefix((i, )):
                if numbers >= 2:
                    # print(f'discarding approx {estimate_num_sums(numbers - 1, the_sum - 1)} for {the_sum - 1, numbers - 1}')
                    pass
                continue
            for r in get_sums_to(the_sum - i, numbers - 1, lambda t: check_prefix((i, *t))):
                yield i, *r


# length of yielded list:
# numbers = 1 -> 1
# numbers = 2 -> the_sum
# numbers = 3 -> the_sum + (the_sum - 1) + ... + 1
#  --> ~= the_sum² / 2
# numbers = 4 -> the_sum² / 2 + (the_sum - 1)² / 2 + ... +
# --> = 1/2 * the_sum³/3
# numbers = 5 -> 1/6 * 1/4 * the_sum⁴
# so in general, 1 / (numbers - 1)! * the_sum^{numbers}

def estimate_num_sums(numbers, the_sum):
    if numbers == 0:
        return float('-inf')
    if numbers == 1:
        return 1
    elif numbers == 2:
        return the_sum
    return the_sum ** numbers / factorial(numbers - 1)


def gcd_of_list(els):
    if not els:
        raise ValueError('Cannot compute gcd of empty list')
    if len(els) == 1:
        return els[0]
    return reduce(gcd, els[1:], els[0])



def dynamic_splitting_search(buttons, dimensions, joltage, depth=0):
    if all((c == 0 for c in joltage)):
        return 0
    if not buttons:
        # but joltage remaining: no solution
        return float('inf')
    if any((c < 0 for c in joltage)):
        return float('inf')

    # find the coordinate for which the fewest number of buttons contribute
    least_popular_dimension = min((
        (i, estimate_num_sums(len([b for b in buttons if b[i] != 0]), joltage[i]))
        for i in range(dimensions)
        if joltage[i] != 0
    ), key=lambda pr: pr[1])[0]
    interested_buttons = [b for b in buttons if b[least_popular_dimension] != 0]
    if not interested_buttons:
        # there is joltage remaining, but none of the buttons contributes
        return float('inf')

    if sum(joltage) % gcd_of_list(list(map(sum, buttons))) != 0:
        # print(f'Found impossibility because of gcd: {sum(joltage)} {len(buttons)}')
        return float('inf')

    remaining_buttons = list(set(buttons).difference(set(interested_buttons)))
    interested_button_usage = joltage[least_popular_dimension]
    if depth < 2:
        pass
        # print(depth * ' ' + f'dyn splitting to:{estimate_num_sums(len(interested_buttons), interested_button_usage)}')
    return min((
        dynamic_splitting_search(remaining_buttons, dimensions, sub_coord(
            joltage,
            reduce(add_coord, (
                mul_coord(b, m)
                for b, m in zip(interested_buttons, comb)
            ), (0,) * dimensions)
        ), depth=depth+1) + interested_button_usage
        for comb in get_sums_to(
            interested_button_usage,
            len(interested_buttons),
            lambda t: all((
                c >= 0
                for c in sub_coord(
                    joltage,
                    reduce(add_coord, (
                        mul_coord(b, m)
                        for b, m in zip(interested_buttons, t)
                    ))
                )
            ))
        )
    ))


def solve_via_intprog(buttons, dimensions, joltage):
    A_eq = [[buttons[i][j] for i in range(len(buttons))] for j in range(dimensions)]
    b_eq = list(joltage)
    # this is almost cheating, so easy
    return sp.optimize.linprog(
        [1] * len(buttons),
        A_eq=A_eq,
        b_eq=b_eq,
        integrality=1
    ).fun


def compute_pt2(parsed_inputs):
    total = 0
    for i, (lights, buttons, dimensions, joltage) in enumerate(parsed_inputs):
        result = solve_via_intprog(buttons, dimensions, joltage)
        # dynamic_splitting_search(buttons, dimensions, joltage)
        # direct_dynamic(sorted(buttons), dimensions, joltage)
        print(i, result)
        total += result
    return total


def main():
    parsed_inputs = parse_input(TEST_INPUT)
    # print(compute_pt1(parsed_inputs))
    # print(list(get_sums_to(3, 2)))
    print(compute_pt2(parsed_inputs))
    with open('input/day10.txt') as f:
        parsed_inputs = parse_input(f.read())
    # print(compute_pt1(parsed_inputs))
    print(compute_pt2(parsed_inputs))

# (0,3,4) (0,2,3) (0,1,2,3,4) {25,1,15,25,11}
# -->
# (0,3,4) (0,2,3) {24,0,14,24,10}
# ->
# (0,3,4) {10, 0, 10, 10}


if __name__ == '__main__':
    main()