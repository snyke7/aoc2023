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


def count_valid_single_arrangements(mask, piece):
    total = 0
    for i in range(len(mask) - piece + 1):
        if i - 1 >= 0 and mask[i - 1] == '#':  # we are not covering a place that needs to be covered
            break
        if i + piece < len(mask) and mask[i + piece] == '#':  # conflict
            continue
        tail = mask[i + piece + 1:]
        if '#' not in tail:
            total += 1
    return total


def count_mask_piece_arrangements_opt(mask_pieces, piece_count, debug=False):
    if len(piece_count) == 0:
        return 1 if not any(('#' in piece for piece in mask_pieces)) else 0
    if sum((1 if el == '#' else 0 for piece in mask_pieces for el in piece)) > sum(piece_count):
        return 0
    masks_with_pieces = [piece for piece in mask_pieces if '#' in piece]
    if len(masks_with_pieces) > len(piece_count):
        return 0
    elif len(masks_with_pieces) == len(piece_count) and len(piece_count) > 1:
        # every piece goes with its exact mask
        result = 1
        for mask, piece in zip(masks_with_pieces, piece_count):
            result *= count_mask_piece_arrangements_opt([mask], [piece])
            if result == 0:
                break
        return result
    if len(piece_count) == 1 and len(masks_with_pieces) == 0:
        pass
    if get_required_space_in_blocks(piece_count, len(mask_pieces)) > sum(map(len, mask_pieces)):
        return 0
    if mask_pieces[0][0] != '#' and mask_pieces[-1] and mask_pieces[-1][-1] == '#':
        # flip around
        mask_pieces = [piece[::-1] for piece in mask_pieces[::-1]]
        piece_count = piece_count[::-1]
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
        if cut_mask and (len(piece_count) == 1 or len(cut_mask) >= piece_count[1]):
            # print('am there')
            next_mask_pieces = [cut_mask] + mask_pieces[1:]
            total_arrangements += count_mask_piece_arrangements(next_mask_pieces, piece_count[1:], debug=debug)
        else:
            next_mask_pieces = mask_pieces[1:]
            mult = count_valid_single_arrangements(first_mask[i:], first_piece)
            # print(f'am here, mult: {mult}, {first_mask}, {first_piece}, {next_mask_pieces}, {piece_count[1:]}')
            total_arrangements += mult * count_mask_piece_arrangements(
                next_mask_pieces, piece_count[1:], debug=debug)
            break
    if '#' not in first_mask:
        total_arrangements += count_mask_piece_arrangements(mask_pieces[1:], piece_count, debug=debug)
    return total_arrangements


def count_arrangements_opt(row, debug=False):
    mask, _, piece_count_raw = row.partition(' ')
    mask_pieces = [el for el in mask.split('.') if el]
    piece_count = [int(part) for part in piece_count_raw.split(',')]
    return count_mask_piece_arrangements_opt(mask_pieces, piece_count, debug=debug)


RESULT_PT1_HASH = -6491710965772637794


def main():
    with open('input/day12_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    # print(count_arrangements('??????#??#?.?# 2,2,2,1'))
    # print(count_arrangements_opt('??????#??#?.?# 2,2,2,1'))
    # row_arrangement_counts_orig = [count_arrangements(row.strip()) for row in input_lines]
    # row_arrangement_counts = [count_arrangements_opt(row.strip()) for row in input_lines]
    # print(sum(row_arrangement_counts_orig))  # 7843
    # print(sum(row_arrangement_counts))  # 7843
    # if hash(tuple(row_arrangement_counts)) != hash(tuple(row_arrangement_counts_orig)):
    #     for i, (l, r) in enumerate(zip(row_arrangement_counts_orig, row_arrangement_counts)):
    #         if l != r:
    #             print(i, input_lines[i])
    #             break
    row_arrangement_counts_big = []
    for i, row in enumerate(input_lines):
        mask, _, piece_count = row.partition(' ')
        big_row = '?'.join(5 * [mask]) + ' ' + ','.join(5 * [piece_count.strip()])
        result = count_arrangements_opt(big_row)
        print(i + 1, result)
        row_arrangement_counts_big.append(result)
    print(sum(row_arrangement_counts_big))

    # new idea: divide pieces over masks before hand, to be sure you do not get redundant computations
    # i.e.
    # given a mask and a set of pieces, calculate possibilities
    # and do so for the remaining masks
    # and go through all pieces possibly contained in this mask


if __name__ == '__main__':
    main()
