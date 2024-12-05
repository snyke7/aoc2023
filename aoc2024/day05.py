TEST_INPUT = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''


def is_before(head, tail, order_rel):
    for that in tail:
        if (that, head) in order_rel:
            return False
    return True


def is_ordered(line, order_rel):
    for i, this in enumerate(line):
        if not is_before(this, line[i+1:], order_rel):
            return False
    return True


def bubble_order(line, order_rel):
    # complexity is terrible but it is simple, and the lines are rather short anyway
    swapped_something = True
    while swapped_something:
        swapped_something = False
        for i in range(len(line)):
            if not is_before(line[i], line[i+1:], order_rel):
                # swap em
                tmp = line[i+1]
                line[i + 1] = line[i]
                line[i] = tmp
                swapped_something = True
    return line


def main():
    test_input = TEST_INPUT
    with open('input/day05.txt') as f:
        test_input = f.read()
    ordering, _, manuals_raw = test_input.partition('\n\n')
    order_rel = {
        (int(line.partition('|')[0]), int(line.strip().partition('|')[2]))
        for line in ordering.splitlines()
    }
    manuals = [list(map(int, line.strip().split(','))) for line in manuals_raw.splitlines() if line.strip()]
    the_sum1 = sum((
        manual[len(manual) // 2]
        for manual in manuals
        if is_ordered(manual, order_rel)
    ))
    print(the_sum1)
    the_sum2 = sum((
        bubble_order(manual, order_rel)[len(manual) // 2]
        for manual in manuals
        if not is_ordered(manual, order_rel)
    ))
    print(the_sum2)


if __name__ == '__main__':
    main()
