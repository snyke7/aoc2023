def extend_dict(base_dict):
    for key in ['red', 'green', 'blue']:
        if key not in base_dict:
            base_dict[key] = 0
    return base_dict


def parse_game(line):
    return [
        extend_dict({
            el.strip().split(' ')[1]: int(el.strip().split(' ')[0])
            for el in gameset.split(',')
        })
        for gameset in line.split(';')
    ]


def parse_game_lines(lines):
    return {
        (i + 1): parse_game(line.split(':')[1])
        for i, line in enumerate(lines)
    }


def is_subset_possible_with_bag(subset, bag):
    return all((subset[color] <= bag_amnt for color, bag_amnt in bag.items()))


def is_game_possible_with_bag(game, bag):
    return all((is_subset_possible_with_bag(subset, bag) for subset in game))


def get_minimum_bag_for_game(game):
    base = extend_dict({})
    for subset in game:
        for col, amnt in subset.items():
            if base[col] < amnt:
                base[col] = amnt
    return base


def get_game_power(game):
    power = 1
    for val in get_minimum_bag_for_game(game).values():
        power *= val
    return power


def main():
    with open('input/day02_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.splitlines()
    games = parse_game_lines(input_lines)
    print(games)
    bag = {'red': 12, 'green': 13, 'blue': 14}
    print(sum((gameid for gameid, game in games.items() if is_game_possible_with_bag(game, bag))))
    print(sum(get_game_power(game) for game in games.values()))


if __name__ == '__main__':
    main()
