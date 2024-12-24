TEST_INPUT1 = '''1
10
100
2024
'''


TEST_INPUT2 = '''1
2
3
2024
'''


def mix(secret, ingredient):
    return secret ^ ingredient


MODULO = 16777216


def prune(secret):
    return secret % MODULO


def evolve(secret):
    secret = mix(secret, secret * 64)
    secret = prune(secret)

    secret = mix(secret, secret // 32)
    secret = prune(secret)

    secret = mix(secret, secret * 2048)
    secret = prune(secret)

    return secret


def get_evolutions(seed, amount):
    result = [seed]
    for _ in range(amount):
        result.append(evolve(result[-1]))
    return result


def get_prices(seed, amount):
    return [secret % 10 for secret in get_evolutions(seed, amount)]


def get_four_diff_map(prices):
    diffs = [price2 - price1 for price1, price2 in zip(prices[:-1], prices[1:])]
    result = {}
    for i in range(4, len(prices)):
        key = tuple(diffs[i - 4:i])
        if key in result:
            continue
        result[key] = prices[i]
    return result


def update_diff_map(diff_map, new_diff_map):
    for key, val in new_diff_map.items():
        if key not in diff_map:
            diff_map[key] = 0
        diff_map[key] += val


def find_key_highest_value(diff_map):
    highest_val = float('-inf')
    the_key = None
    for key, val in diff_map.items():
        if val > highest_val:
            highest_val = val
            the_key = key
    return the_key


def main():
    test_input = TEST_INPUT2.splitlines()
    with open('input/day22.txt') as f:
        test_input = f.readlines()
    seeds = [int(line.strip()) for line in test_input if line.strip()]
    print(sum((get_evolutions(seed, 2000)[-1] for seed in seeds)))

    diff_map = {}
    for seed in seeds:
        prices = get_prices(seed, 2000)
        new_diff_map = get_four_diff_map(prices)
        update_diff_map(diff_map, new_diff_map)
    high_key = find_key_highest_value(diff_map)
    print(high_key, diff_map[high_key])


if __name__ == '__main__':
    main()
