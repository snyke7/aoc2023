TEST_INPUT = '''2333133121414131402'''


def defragment_pt1(alt_block_free):
    result = [None] * (sum(alt_block_free[::2]))
    front_result_idx = 0
    front = 0
    back = len(alt_block_free) - 1
    rem_back = alt_block_free[back]
    rem_front = 0
    while front < back:
        for i in range(alt_block_free[front]):
            result[front_result_idx + i] = front // 2
        front_result_idx += alt_block_free[front]
        front += 1
        if front == back:
            break
        rem_front = alt_block_free[front]
        while rem_front > 0 and front < back:
            new_els = min(rem_back, rem_front)
            for i in range(new_els):
                result[front_result_idx + i] = back // 2
                rem_back -= 1
                rem_front -= 1
            front_result_idx += new_els
            if rem_back == 0:
                back -= 2
                rem_back = alt_block_free[back]
        front += 1
    # if front == back, we might still have rem_back
    if rem_front == 0:
        while rem_back > 0:
            result[front_result_idx] = back // 2
            front_result_idx += 1
            rem_back -= 1
    return result


def defragment_pt2(alt_block_free):
    result = [None] * (sum(alt_block_free))
    front_result_idx = 0
    free_spaces = {}
    for i in range(len(alt_block_free)):
        if i % 2 == 0:
            for j in range(alt_block_free[i]):
                result[front_result_idx + j] = i // 2
        else:
            free_spaces[i // 2] = (front_result_idx, alt_block_free[i])
        front_result_idx += alt_block_free[i]
    back = len(alt_block_free) - 1
    while back > 0:
        for i in range(back // 2):
            result_idx, free = free_spaces[i]
            if free >= alt_block_free[back]:
                for j in range(alt_block_free[back]):
                    result[result_idx + j] = back // 2
                    result[sum(alt_block_free[:back]) + j] = None
                free_spaces[i] = (result_idx + alt_block_free[back]), free - alt_block_free[back]
                break
        back -= 2
        # print(result)
    return result


def checksum(result):
    return sum((
        pos * idx
        for pos, idx in
        enumerate(result)
        if idx is not None
    ))


def main():
    test_input = TEST_INPUT
    with open('input/day09.txt') as f:
        test_input = f.read()
    alt_block_free = list(map(int, test_input.strip()))
    # print(alt_block_free)
    # print(alt_block_free[::2])
    result = defragment_pt1(alt_block_free)
    # print(result.count(5256))
    # print(result)
    print(checksum(result))
    result = defragment_pt2(alt_block_free)
    # print(result.count(5256))
    # print(result)
    print(checksum(result))


if __name__ == '__main__':
    main()
