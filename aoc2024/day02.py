TEST_INPUT = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''


def is_safe(report_diff):
    if report_diff[0] == 0:
        return False
    if report_diff[0] < 0:
        if any((diff > 0 for diff in report_diff)):
            return False
    if report_diff[0] > 0:
        if any((diff < 0 for diff in report_diff)):
            return False
    abs_diffs = list(map(abs, report_diff))
    return all((1 <= diff <= 3 for diff in abs_diffs))


def make_report_diff(report):
    return [n - l for n, l in zip(report[1:], report[:-1])]

def is_safe_pt2(report):
    return any((is_safe(make_report_diff(report[:i] + report[i+1:])) for i in range(len(report))))


def main():
    test_input = TEST_INPUT.splitlines()
    # with open('input/day02.txt') as f:
    #     test_input = f.readlines()
    reports = [list(map(int, line.strip().split(' '))) for line in test_input]
    diffs = [make_report_diff(report) for report in reports]
    print(sum((1 for diff in diffs if is_safe(diff))))
    print(sum((1 for report in reports if is_safe_pt2(report))))

if __name__ == '__main__':
    main()
