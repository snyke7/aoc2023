CARD_ORDER_PT1 = {c: i for i, c in enumerate(list('AKQJT98765432'))}
CARD_ORDER_PT2 = {c: i for i, c in enumerate(list('AKQT98765432J'))}


def get_hand_as_int(hand, card_order):
    result = 0
    for i, c in enumerate(hand):
        result += (12 - card_order[c]) * 13 ** (4 - i)
    return result


def get_hand_as_int_pt1(hand):
    return get_hand_as_int(hand, CARD_ORDER_PT1)


def get_rev_count_dict(hand):
    count_dict = {c: 0 for c in CARD_ORDER_PT1.keys()}
    for c in hand:
        count_dict[c] += 1
    rev_count_dict = {i: [] for i in range(6)}
    for c, num in count_dict.items():
        if num != 0:
            rev_count_dict[num] = rev_count_dict[num] + [c]
    for num, cards in list(rev_count_dict.items()):
        if not cards:
            del rev_count_dict[num]
    return rev_count_dict


def get_hand_type(rev_count_dict):
    # 6 five of a kind >
    # 5 four of a kind >
    # 4 full house >
    # 3 three of a kind >
    # 2 two pair >
    # 1 one pair >
    # 0 'high card'
    if 5 in rev_count_dict:
        return 6
    elif 4 in rev_count_dict:
        return 5
    elif 3 in rev_count_dict and 2 in rev_count_dict:
        return 4
    elif 3 in rev_count_dict:
        return 3
    elif 2 in rev_count_dict:
        return len(rev_count_dict[2])  # two or one pair
    else:
        return 0


def get_hand_score_pt1(hand):
    rev_count_dict = get_rev_count_dict(hand)
    return get_hand_type(rev_count_dict) * 13 ** 5 + get_hand_as_int_pt1(hand)


def get_hand_score_pt2(hand):
    rev_count_dict = get_rev_count_dict(hand)
    # 6 five of a kind >
    # 5 four of a kind >
    # 4 full house >
    # 3 three of a kind >
    # 2 two pair >
    # 1 one pair >
    # 0 'high card'
    if 'J' not in hand:
        return get_hand_type(rev_count_dict) * 13 ** 5 + get_hand_as_int(hand, CARD_ORDER_PT2)
    # otherwise, first inspect the hand type without the J
    stripped_hand = [c for c in hand if c != 'J']
    stripped_type = get_hand_type(get_rev_count_dict(stripped_hand))
    joker_count_upgrade_dict = {
        1: {
            0: 1,  # high card to 1 pair
            1: 3,  # one pair to 3 of a kind
            2: 4,  # two pair to full house
            3: 5,  # 3 of a kind to 4 of a kind
            5: 6,  # 4 of a kind to 5 of a kind
            # full house (4) and 5 of a kind (6) not possible
        },
        2: {
            0: 3,  # high card to 3 of a kind
            1: 5,  # one pair to 4 of a kind
            3: 6,  # 3 of a kind to 5 of a kind
            # other options not possible
        },
        3: {
            0: 5,  # high card to 4 of a kind
            1: 6,  # one pair to 5 of a kind
        },
        4: {
            0: 6,  # high card to 5 of a kind
        },
        5: {
            0: 6,  # empty hand is also seen as high card, becomes 5 of a kind
        }
    }
    joker_count = sum((1 for c in hand if c == 'J'))
    return joker_count_upgrade_dict[joker_count][stripped_type] * 13 ** 5 + get_hand_as_int(hand, CARD_ORDER_PT2)


def part1(hand_lines):
    hands = [(line.split(' ')[0], int(line.split(' ')[1][:])) for line in hand_lines]
    hands_with_scores = sorted([
        (hand, get_hand_score_pt1(hand), bid)
        for hand, bid in hands
    ], key=lambda pr: pr[1])
    total_part1 = sum((score * (i + 1) for i, (_, _, score) in enumerate(hands_with_scores)))
    print(total_part1)


def part2(hand_lines):
    hands = [(line.split(' ')[0], int(line.split(' ')[1][:])) for line in hand_lines]
    hands_with_scores = sorted([
        (hand, get_hand_score_pt2(hand), bid)
        for hand, bid in hands
    ], key=lambda pr: pr[1])
    total_part2 = sum((score * (i + 1) for i, (_, _, score) in enumerate(hands_with_scores)))
    print(total_part2)


def main():
    with open('input/day07_input.txt') as f:
        hand_lines = f.readlines()
    hand_lines2 = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''.splitlines()
    part1(hand_lines)
    part2(hand_lines)


if __name__ == '__main__':
    main()
