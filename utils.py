from itertools import product
from typing import TypeVar, Dict, List, Tuple

from collections import defaultdict


A = TypeVar('A')


def dijkstra(graph: Dict[A, List[Tuple[A, int]]], start: A) -> Dict[A, int]:
    result = {start: 0}
    new = [start]
    while new:
        node = new.pop(0)
        cost = result[node]
        for neigbor, dist in graph[node]:
            if neigbor not in result or result[neigbor] > cost + dist:
                result[neigbor] = cost + dist
                new.append(neigbor)
    return result


def step_to_dist_graph(graph: Dict[A, List[A]]) -> Dict[A, List[Tuple[A, int]]]:
    return {a: [(b, 1) for b in neighbors] for a, neighbors in graph.items()}


def dijkstra_steps(graph: Dict[A, List[A]], start: A) -> Dict[A, int]:
    return dijkstra(step_to_dist_graph(graph), start)


def file_read_lines(filename: str):
    with open(filename) as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def file_read(filename: str):
    with open(filename) as f:
        return f.read()


Coord2 = Tuple[int, int]
UP2 = (-1, 0)
DOWN2 = (1, 0)
LEFT2 = (0, -1)
RIGHT2 = (0, 1)
# ordered with an anti-clockwise rotation
DIRECTIONS2 = [DOWN2, RIGHT2, UP2, LEFT2]


def add_coord(base: Tuple[int, ...], move: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(map(sum, zip(base, move)))


def sub_coord(base: Tuple[int, ...], sub: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(map(sum, zip(base, map(lambda c: -1*c, sub))))


def dijkstra_steps_path(graph: Dict[A, List[A]], start: A) -> Dict[A, Tuple[int, List[A]]]:
    result = {start: (0, [start])}
    new = [start]
    while new:
        node = new.pop(0)
        cost, path = result[node]
        for neigbor in graph[node]:
            if neigbor not in result or result[neigbor][0] > cost + 1:
                result[neigbor] = cost + 1, path + [neigbor]
                new.append(neigbor)
    return result


def dijkstra_path(graph: Dict[A, List[Tuple[A, int]]], start: A) -> Dict[A, Tuple[int, List[A]]]:
    result = {start: (0, [start])}
    new = [start]
    while new:
        node = new.pop(0)
        cost, path = result[node]
        for neigbor, dist in graph[node]:
            if neigbor not in result or result[neigbor][0] > cost + dist:
                result[neigbor] = cost + dist, path + [neigbor]
                new.append(neigbor)
    return result


def dijkstra_all_paths(graph: Dict[A, List[Tuple[A, int]]], start: A) -> Dict[A, Tuple[int, List[List[A]]]]:
    result = {start: (0, [[start]])}
    new = [start]
    while new:
        node = new.pop(0)
        cost, paths = result[node]
        for neighbor, dist in graph[node]:
            if neighbor not in result or result[neighbor][0] > cost + dist:
                # we found a new or shorter path
                result[neighbor] = cost + dist, [path + [neighbor] for path in paths]
                new.append(neighbor)
            elif neighbor in result and result[neighbor][0] == cost + dist:
                # we found a new path
                _, existing_paths = result[neighbor]
                result[neighbor] = cost + dist, existing_paths + [path + [neighbor] for path in paths]
    return result

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
    print(f'utils.py: Sieving primes until {sieved_until}')
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
