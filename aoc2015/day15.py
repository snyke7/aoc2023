from attrs import define


TEST_INPUT = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
'''


@define
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse_ingredient(line):
    name, _, tail = line.partition(': capacity ')
    capacity, _, tail = tail.partition(', durability ')
    durability, _, tail = tail.partition(', flavor ')
    flavor, _, tail = tail.partition(', texture ')
    texture, _, calories = tail.partition(', calories ')
    return Ingredient(name, int(capacity), int(durability), int(flavor), int(texture), int(calories))


def get_sums_to(amt, length):
    if length == 1:
        yield [amt]
        return
    for a in range(amt + 1):
        for s in get_sums_to(amt - a, length - 1):
            yield [a] + s


def get_dunk_score(ingredients, c):
    capacity = max(sum((i.capacity * a for i, a in zip(ingredients, c))), 0)
    durability = max(sum((i.durability * a for i, a in zip(ingredients, c))), 0)
    flavor = max(sum((i.flavor * a for i, a in zip(ingredients, c))), 0)
    texture = max(sum((i.texture * a for i, a in zip(ingredients, c))), 0)
    return capacity * durability * flavor * texture


def get_dunkiest(ingredients):
    return max((get_dunk_score(ingredients, c) for c in get_sums_to(100, len(ingredients))))


def get_calories(ingredients, c):
    return sum((i.calories * a for i, a in zip(ingredients, c)))


def get_dunkiest_500_cal(ingredients):
    return max((
        get_dunk_score(ingredients, c)
        for c in get_sums_to(100, len(ingredients))
        if get_calories(ingredients, c) == 500
    ))


def main():
    test_input = TEST_INPUT
    with open('input/day15.txt') as f:
        test_input = f.read()
    ingredients = [parse_ingredient(line) for line in test_input.splitlines()]
    print(ingredients)
    print(get_dunkiest(ingredients))
    print(get_dunkiest_500_cal(ingredients))


if __name__ == '__main__':
    main()