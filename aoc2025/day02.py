TEST_INPUT = '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'''


def parse_range(range_str):
    head, _, tail = range_str.partition('-')
    return int(head), int(tail)


def parse_ranges(line):
    return [
        parse_range(el)
        for el in line.strip().split(',')
    ]


def is_invalid_id_pt1(the_id):
    el_str = str(the_id)
    if len(el_str) % 2 != 0:
        return False
    pt1 = el_str[:len(el_str) // 2]
    pt2 = el_str[len(el_str) // 2:]
    return pt1 == pt2


def get_invalid_ids(range_pair, invalid_id_fun):
    head, tail = range_pair
    result = set()
    for el in range(head, tail + 1):
        if invalid_id_fun(el):
            result.add(el)
    return result


def get_invalid_ids_sum(ranges, invalid_id_fun=is_invalid_id_pt1):
    result = 0
    for range_pair in ranges:
        for invalid_id in get_invalid_ids(range_pair, invalid_id_fun):
            result += invalid_id
    return result


def is_invalid_id_pt2(the_id):
    el_str = str(the_id)
    for d in range(1, len(el_str)):
        if len(el_str) % d != 0:
            continue
        pt1 = el_str[:d]
        is_repetition = True
        for j in range(1, len(el_str) // d):
            ptj = el_str[j*d:j*d+d]
            if pt1 != ptj:
                is_repetition = False
                break
        if is_repetition:
            return True
    return False



def main():
    ranges = parse_ranges(TEST_INPUT)
    print(get_invalid_ids_sum(ranges))
    print(get_invalid_ids_sum(ranges, is_invalid_id_pt2))
    with open('input/day02.txt') as f:
        ranges = parse_ranges(f.read())
    print(get_invalid_ids_sum(ranges))
    print(get_invalid_ids_sum(ranges, is_invalid_id_pt2))


if __name__ == '__main__':
    main()