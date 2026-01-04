TEST_INPUT = '''20
15
10
5
5
'''


def get_container_combinations(total, containers):
    if total == 0:
        yield []
    for i, c in enumerate(containers):
        if c > total:
            continue
        for comb in get_container_combinations(total - c, containers[i + 1:]):
            yield [c] + comb


def main():
    container_text = TEST_INPUT
    containers = list(map(int, container_text.splitlines()))
    print(len(list(get_container_combinations(25, containers))))

    with open('input/day17.txt') as f:
        container_text = f.read()
    containers = list(map(int, container_text.splitlines()))
    combs = list(get_container_combinations(150, containers))
    print(len(combs))

    min_container_use = min(map(len, combs))
    print(len([c for c in combs if len(c) == min_container_use]))


if __name__ == '__main__':
    main()
