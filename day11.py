TEST1 = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''


def calc_total_galaxy_dist(galaxies, row_len, col_len, empty_dist):
    row_crossing_dist = {i: empty_dist for i in range(row_len)}
    col_crossing_dist = {j: empty_dist for j in range(col_len)}
    for i, j in galaxies:
        row_crossing_dist[i] = 1
        col_crossing_dist[j] = 1
    total_dist = 0
    for n, (this_x, this_y) in enumerate(galaxies):
        for m, (that_x, that_y) in enumerate(galaxies[n+1:]):
            dist = 0
            for row in range(this_x, that_x, 1 if that_x > this_x else -1):
                dist += row_crossing_dist[row]
            for col in range(this_y, that_y, 1 if that_y > this_y else -1):
                dist += col_crossing_dist[col]
            total_dist += dist
    return total_dist


def main():
    with open('input/day11_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST1.splitlines()
    galaxies = [
        (i, j)
        for i, line in enumerate(input_lines)
        for j, el in enumerate(line.strip())
        if el == '#'
    ]
    print(calc_total_galaxy_dist(galaxies, len(input_lines), len(input_lines[0].strip()), 2))
    print(calc_total_galaxy_dist(galaxies, len(input_lines), len(input_lines[0].strip()), 1000000))


if __name__ == '__main__':
    main()
