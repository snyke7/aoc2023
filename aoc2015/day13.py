from collections import defaultdict
from itertools import permutations


TEST_INPUT = '''Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
'''


def parse_line(the_line):
    name, _, tail = the_line.partition(' would ')
    diff_str, _, the_name = tail.strip()[:-1].partition(' happiness units by sitting next to ')
    diff_sign, _, diff_amt_str = diff_str.partition(' ')
    diff_amt = int(diff_amt_str) * (1 if diff_sign == 'gain' else -1)
    return name, the_name, diff_amt


def get_happiness_dict(test_input):
    result_dict = defaultdict(lambda: 0)
    names = set()
    for left, right, diff in (parse_line(line) for line in test_input.splitlines()):
        names.add(left)
        names.add(right)
        result_dict[frozenset((left, right))] += diff
    return list(sorted(names)), dict(result_dict)


def get_happiness(comb, neighbor_score):
    result = 0
    for left, right in zip(comb, comb[1:] + [comb[0]]):
        result += neighbor_score[frozenset((left, right))]
    return result


def get_best_seating(names, neighbor_score):
    best_happiness = -1
    best_comb = None
    for comb_tail in permutations(names[1:], len(names) - 1):
        comb = [names[0]] + list(comb_tail)
        this_happiness = get_happiness(comb, neighbor_score)
        if this_happiness > best_happiness:
            best_happiness = this_happiness
            best_comb = comb
    return best_happiness




def main():
    test_input = TEST_INPUT
    with open('input/day13.txt') as f:
        test_input = f.read()
    names, neighbor_score = get_happiness_dict(test_input)
    print(get_best_seating(names, neighbor_score))
    # part 2
    for name in names:
        neighbor_score[frozenset((name, 'Ike'))] = 0
    names.append('Ike')
    print(get_best_seating(names, neighbor_score))



if __name__ == '__main__':
    main()
