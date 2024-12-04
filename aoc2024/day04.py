import re


TEST_INPUT = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''


BARE_INPUT = '''....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
'''

BARE_INPUT2 = '''.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
'''


def count_xmas_line(the_line):
    return len(re.findall('XMAS', the_line)) + len(re.findall('SAMX', the_line))


def count_xmas_lines(the_lines):
    return sum((count_xmas_line(the_line) for the_line in the_lines))


def get_ul_dr_diags(the_lines):
    return [
        ''.join([
            the_lines[j][j - i]
            for j in range(min(len(the_lines), len(the_lines[0])))
            if j - i < len(the_lines[j])
        ])
        for i in range(-1*len(the_lines[0]) + 1, 0)
    ] + [
        ''.join([
            the_lines[j + i][j]
            for j in range(min(len(the_lines), len(the_lines[0])))
            if j + i < len(the_lines)
        ])
        for i in range(0, len(the_lines))
    ]


def get_ur_dl_diags(the_lines):
    return get_ul_dr_diags([
        list(reversed(the_line))
        for the_line in the_lines
    ])


def count_all_xmas(the_lines):
    # horizontal
    result = count_xmas_lines(the_lines)
    # vertical
    result += count_xmas_lines([''.join((the_lines[i][j] for i in range(len(the_lines)))) for j in range(len(the_lines[0]))])
    # diagonal UL -> DR
    diagonals_ul_dr = get_ul_dr_diags(the_lines)
    result += count_xmas_lines(diagonals_ul_dr)
    # UR -> DL
    diagonals_ur_dl = get_ur_dl_diags(the_lines)
    result += count_xmas_lines(diagonals_ur_dl)
    return result


def count_x_mas_line(line, prev_line, next_line):
    result = 0
    for match in list(re.finditer('MAS', line)) + list(re.finditer('SAM', line)):
        m_index = match.start()
        a_index = m_index + 1
        if prev_line[a_index] == 'M' and next_line[a_index] == 'S':
            result += 1
        elif prev_line[a_index] == 'S' and next_line[a_index] == 'M':
            result += 1
    return result


def count_x_mas_lines(the_lines):
    return sum((
        count_x_mas_line(line, prev_line, next_line)
        for line, prev_line, next_line in
        zip(the_lines[1:-1], the_lines[0:-2], the_lines[2:])
    ))


def count_all_x_mas(the_lines):
    # horizontal + vertical
    result = 0  # count_x_mas_lines(the_lines)
    # print(result)
    diags = get_ul_dr_diags(the_lines)
    # main diagonals
    diags1 = [
        '.'*((len(the_lines) - len(diag)) // 2) + diag + '.'*((len(the_lines) - len(diag)) // 2)
        for diag in diags[::2]
    ]
    result += count_x_mas_lines(diags1)
    # off by one diagonals
    diags2 = [
        '.'*((len(the_lines) + 1 - len(diag)) // 2) + diag + '.'*((len(the_lines) + 1 - len(diag)) // 2)
        for diag in diags[1::2]
    ]
    result += count_x_mas_lines(diags2)
    return result


def main():
    test_input = TEST_INPUT.splitlines()
    with open('input/day04.txt') as f:
        test_input = [line.strip() for line in f.readlines() if line.strip()]
    print(count_all_xmas(test_input))
    # 1863 < answer < 1909
    print(count_all_x_mas(test_input))


if __name__ == '__main__':
    main()