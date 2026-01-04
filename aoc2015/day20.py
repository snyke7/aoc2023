from utils import get_divisors

LOWER_BOUND_PRESENTS = 33100000


def calc_presents(num):
    return 10 * sum((div for div in get_divisors(num)))


def calc_presents_pt2(num):
    return 11 * sum((
        div
        for div in get_divisors(num)
        if num // div <= 50
    ))


def find_first_house_with_at_least(min_presents, present_calc=calc_presents):
    num = 1
    while present_calc(num) < min_presents:
        num += 1
    return num


def main():
    print(find_first_house_with_at_least(LOWER_BOUND_PRESENTS))
    print(find_first_house_with_at_least(LOWER_BOUND_PRESENTS, present_calc=calc_presents_pt2))


if __name__ == '__main__':
    main()