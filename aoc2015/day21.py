from attrs import define


SHOP_INPUT = '''Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
'''


@define
class ShopItem:
    name: str
    cost: int
    damage: int
    armor: int


def parse_shop_item(item_line):
    non_spaces = [el for el in item_line.strip().split(' ') if el]
    cost, damage, armor = tuple(map(int, non_spaces[-3:]))
    return ShopItem(' '.join(non_spaces[:-3]), cost, damage, armor)


def parse_shop(shop_input):
    weapon_raw, armor_raw, rings_raw = tuple(shop_input.split('\n\n'))
    weapons = [parse_shop_item(line) for line in weapon_raw.splitlines()[1:]]
    armor = [parse_shop_item(line) for line in armor_raw.splitlines()[1:]]
    rings = [parse_shop_item(line) for line in rings_raw.splitlines()[1:]]
    return weapons, armor, rings


WEAPONS, ARMOR, RINGS = parse_shop(SHOP_INPUT)


def get_valid_weapons():
    for weap in WEAPONS:
        yield [weap]


def get_valid_armors():
    yield []
    for item in ARMOR:
        yield [item]


def get_valid_rings():
    yield []
    for ring in RINGS:
        yield [ring]
    for i, left in enumerate(RINGS):
        for right in RINGS[i+1:]:
            yield [left, right]


def get_valid_equips():
    for weps in get_valid_weapons():
        for eq in get_valid_armors():
            for rings in get_valid_rings():
                yield weps + eq + rings


@define
class Char:
    name: str
    hp: int
    damage: int
    armor: int

    def receive_blow(self, dmg) -> int:
        actual_dmg = max(1, dmg - self.armor)
        self.hp -= actual_dmg
        return actual_dmg

    def is_dead(self):
        return self.hp <= 0


def does_left_win(left: Char, right: Char) -> bool:
    while not left.is_dead():
        right.receive_blow(left.damage)
        if right.is_dead():
            return True
        left.receive_blow(right.damage)
    return False


def get_stingiest_win(make_boss, make_player):
    min_cost = float('inf')
    for eq in get_valid_equips():
        cost = sum((i.cost for i in eq))
        dmg = sum((i.damage for i in eq))
        armor = sum((i.armor for i in eq))
        player = make_player()
        boss = make_boss()
        player.damage += dmg
        player.armor += armor
        if does_left_win(player, boss) and cost < min_cost:
            min_cost = cost
    return min_cost


def get_most_expensive_loss(make_boss, make_player):
    max_cost = float('-inf')
    for eq in get_valid_equips():
        cost = sum((i.cost for i in eq))
        dmg = sum((i.damage for i in eq))
        armor = sum((i.armor for i in eq))
        player = make_player()
        boss = make_boss()
        player.damage += dmg
        player.armor += armor
        if not does_left_win(player, boss) and cost > max_cost:
            max_cost = cost
    return max_cost


def main():
    with open('input/day21.txt') as f:
        boss_str = f.read()
    boss_nums = tuple((int(line.partition(': ')[2]) for line in boss_str.splitlines()))
    # boss_nums = 12, 7, 2
    make_boss = lambda: Char('BOSS', *boss_nums)
    # me = Char('snyke7', 8, 5, 5)
    make_player = lambda: Char('snyke7', 100, 0, 0)
    print(get_stingiest_win(make_boss, make_player))
    print(get_most_expensive_loss(make_boss, make_player))


if __name__ == '__main__':
    main()
