from functools import lru_cache


TEST = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''


def get_required_contiguous_space(piece_count):  # in a contiguous block!
    return sum(piece_count) + len(piece_count) - 1


def get_required_space_in_blocks(piece_count, num_blocks):
    return get_required_contiguous_space(piece_count) - (num_blocks - 1)


# Original solution for part1: short, but slow
def count_mask_piece_arrangements(mask_pieces, piece_count, debug=False):
    if len(piece_count) == 0:
        return 1 if not any(('#' in piece for piece in mask_pieces)) else 0
    if get_required_space_in_blocks(piece_count, len(mask_pieces)) > sum(map(len, mask_pieces)):
        return 0
    first_mask = mask_pieces[0]
    first_piece = piece_count[0]
    if debug:
        print(mask_pieces, piece_count, first_mask, first_piece)
    total_arrangements = 0
    for i in range(len(first_mask) - first_piece + 1):
        if i - 1 >= 0 and first_mask[i - 1] == '#':
            break
        if i + first_piece < len(first_mask) and first_mask[i + first_piece] == '#':
            continue
        cut_mask = first_mask[i + first_piece + 1:]
        next_mask_pieces = ([cut_mask] if cut_mask else []) + mask_pieces[1:]
        total_arrangements += count_mask_piece_arrangements(next_mask_pieces, piece_count[1:], debug=debug)
    if '#' not in first_mask:
        total_arrangements += count_mask_piece_arrangements(mask_pieces[1:], piece_count, debug=debug)
    return total_arrangements


def count_arrangements(row, debug=False):
    mask, _, piece_count_raw = row.partition(' ')
    mask_pieces = [el for el in mask.split('.') if el]
    piece_count = [int(part) for part in piece_count_raw.split(',')]
    return count_mask_piece_arrangements(mask_pieces, piece_count, debug=debug)


@lru_cache(maxsize=None)
def get_free_ones_placement(one_count, space):
    if space < 0:
        return 0
    if one_count == 0:
        return 1
    elif one_count == 1:
        return space
    else:
        result = 0
        for i in range(space - 2):
            result += get_free_ones_placement(one_count - 1, (space - i) - 2)
        return result


def get_free_placement(piece_count, space):
    return get_free_ones_placement(len(piece_count), space - sum(piece_count) + len(piece_count))


def count_mask_arrangements(mask, piece_count, debug=False):
    if '#' not in mask:
        return get_free_placement(piece_count, len(mask))
    if len(piece_count) == 0:
        return 0 if '#' in mask else 1
    if sum(piece_count) + len(piece_count) - 1 > len(mask):  # this one is quite important
        return 0
    longest_piece = max(piece_count)
    if mask[0] == '#':
        if piece_count[0] > len(mask) or (piece_count[0] < len(mask) and mask[piece_count[0]] == '#'):
            return 0
        else:
            return count_mask_arrangements(mask[piece_count[0] + 1:], piece_count[1:], debug=debug)
    if mask[-1] == '#':
        return count_mask_arrangements(mask[::-1], piece_count[::-1])
    middle = len(mask) // 2 - (1 if len(mask) > 0 else 0)
    middle_piece_start = middle
    while mask[middle_piece_start] == '#' and middle_piece_start >= 0:
        middle_piece_start -= 1
    while middle + 1 < len(mask) and mask[middle + 1] == '#':
        middle += 1
    middle_piece_length = middle - middle_piece_start
    result = 0
    for n in range(min(longest_piece - middle_piece_length + 1, len(mask) - middle)):
        new_masks = [
            mask[:middle + 1] + n * '#',
            mask[middle + 1 + n + 1:]
        ]
        if middle + 1 + n < len(mask) and mask[middle + 1 + n] == '#':
            continue
        if debug:
            print(mask, new_masks, piece_count, middle, n)
        result += count_mask_pieces_arrangements(
            new_masks,
            piece_count,
            debug=debug
        )
    return result


def count_mask_pieces_arrangements(mask_pieces, piece_count, debug=False):
    if len(piece_count) == 0:
        return 0 if any(('#' in piece for piece in mask_pieces)) else 1
    if len(mask_pieces) == 1:
        return count_mask_arrangements(mask_pieces[0], piece_count, debug=debug)
    result = 0
    first_mask = mask_pieces[0]
    for s in range(len(piece_count) + 1):
        mult = count_mask_arrangements(first_mask, piece_count[:s], debug=debug)
        if mult > 0:
            sub_result = count_mask_pieces_arrangements(mask_pieces[1:], piece_count[s:], debug=debug)
            if debug:
                print(mult, first_mask, piece_count[:s], sub_result, mask_pieces[1:], piece_count[s:], s, result)
            result += mult * sub_result
    return result


def count_arrangements_opt(row, debug=False):
    mask, _, piece_count_raw = row.partition(' ')
    mask_pieces = [el for el in mask.split('.') if el]
    piece_count = [int(part) for part in piece_count_raw.split(',')]
    return count_mask_pieces_arrangements(mask_pieces, piece_count, debug=debug)


# Tweaked solution for part1, memoizing for this result
def count_mask_piece_arrangements_memoize(mask_pieces, piece_count, debug=False):
    result_dict = {}
    mask = '.'.join(mask_pieces)

    def go(mask_i, piece_i, current):
        if (mask_i, piece_i, current) in result_dict:
            return result_dict[(mask_i, piece_i, current)]
        if mask_i == len(mask):
            if piece_i == len(piece_count) and current == 0:
                return 1
            elif piece_i == len(piece_count) - 1 and current == piece_count[-1]:
                return 1
            else:
                return 0
        total_arrangements = 0
        for c in ('.', '#'):
            if mask[mask_i] in (c, '?'):
                if c == '.' and current == 0:
                    total_arrangements += go(mask_i + 1, piece_i, current)
                elif c == '.' and current > 0 and piece_i < len(piece_count) and piece_count[piece_i] == current:
                    total_arrangements += go(mask_i + 1, piece_i + 1, 0)
                elif c == '#':
                    total_arrangements += go(mask_i + 1, piece_i, current + 1)
        result_dict[(mask_i, piece_i, current)] = total_arrangements
        return total_arrangements

    return go(0, 0, 0)


def count_arrangements_memoize(row, debug=False):
    mask, _, piece_count_raw = row.partition(' ')
    mask_pieces = [el for el in mask.split('.') if el]
    piece_count = [int(part) for part in piece_count_raw.split(',')]
    return count_mask_piece_arrangements_memoize(mask_pieces, piece_count, debug=debug)


def main():
    with open('input/day12_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()

    # part 1
    row_arrangement_counts_orig = [count_arrangements(row.strip()) for row in input_lines]
    row_arrangement_counts = [count_arrangements_memoize(row.strip()) for row in input_lines]
    print(sum(row_arrangement_counts_orig))  # 7843
    print(sum(row_arrangement_counts))  # should match! 7843
    print()

    # part 2
    multiplier = 5
    row_arrangement_counts_big = []
    for i, row in enumerate(input_lines):  # still takes about 1.5 minutes with pypy :(
        mask, _, piece_count = row.partition(' ')
        big_row = '?'.join(multiplier * [mask]) + ' ' + ','.join(multiplier * [piece_count.strip()])
        result = count_arrangements_memoize(big_row)
        if i % 100 == 99:
            print(i + 1, result)
        row_arrangement_counts_big.append(result)
    print(sum(row_arrangement_counts_big))


if __name__ == '__main__':
    main()
