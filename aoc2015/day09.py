from itertools import permutations


TEST_INPUT = '''London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
'''


def parse_distance(distance_line):
    city1, _, rem = distance_line.partition(' to ')
    city2, _, dist = rem.partition(' = ')
    return city1, city2, int(dist)


def parse_distances(input_lines):
    result = {}
    cities = set()
    for line in input_lines:
        city1, city2, dist = parse_distance(line)
        result[(city1, city2)] = dist
        result[(city2, city1)] = dist
        cities.add(city1)
        cities.add(city2)
    return cities, result


def get_route_length(city_seq, distances):
    return sum((
        distances[(prev_city, next_city)]
        for prev_city, next_city in
        zip(city_seq[:-1], city_seq[1:])
    ))


def get_coolest_route_length(cities, distances, is_cooler, least_cool):
    coolest_route_length = least_cool
    for city_seq in permutations(cities, len(cities)):
        this_route_length = get_route_length(city_seq, distances)
        if is_cooler(this_route_length, coolest_route_length):
            coolest_route_length = this_route_length
    return coolest_route_length


def main():
    test_input = TEST_INPUT.splitlines()
    with open('input/day09_input.txt') as f:
        test_input = f.readlines()
    cities, distances = parse_distances(test_input)
    print(get_coolest_route_length(cities, distances, lambda a, b: a < b, float('inf')))
    print(get_coolest_route_length(cities, distances, lambda a, b: a > b, float('-inf')))


if __name__ == '__main__':
    main()
