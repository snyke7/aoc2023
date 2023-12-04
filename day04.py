def parse_card(line):
    return [
        {int(card) for card in cards.split(' ') if card != ''}
        for cards in line.split('|')
    ]


def parse_card_lines(lines):
    return {
        (i + 1): parse_card(line.split(':')[1].strip())
        for i, line in enumerate(lines)
    }


def total_cards(match_dict):
    multiplier = {}
    for i, matches in match_dict.items():
        if i not in multiplier:
            multiplier[i] = 1
        mult = multiplier[i]
        for j in range(i + 1, i + matches + 1):
            if j not in match_dict:
                break
            if j not in multiplier:
                multiplier[j] = 1
            multiplier[j] += mult
    print(multiplier)
    return sum(multiplier.values())


def main():
    with open('input/day04_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.splitlines()
    pile = parse_card_lines(input_lines)
    matches = {i: len(card[0].intersection(card[1])) for i, card in pile.items()}
    part1 = sum((2 ** (match - 1) for match in matches.values() if match > 0))
    print(part1)
    print(total_cards(matches))


if __name__ == '__main__':
    main()
