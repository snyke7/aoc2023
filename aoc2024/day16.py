from utils import dijkstra, DIRECTIONS2, add_coord, RIGHT2, dijkstra_path, dijkstra_all_paths

TEST_INPUT1 = '''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''

TEST_INPUT2 = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
'''


def read_dist_graph(input_lines):
    result = {}
    start = None
    end = None
    for i, line in enumerate(input_lines):
        for j, el in enumerate(line.strip()):
            if el == '#':
                continue
            if el == 'S':
                start = (i, j, DIRECTIONS2.index(RIGHT2))
            if el == 'E':
                end = (i, j)
                result[end] = []
            for k, direction in enumerate(DIRECTIONS2):
                result[(i, j, k)] = [
                    ((i, j, (k - 1) % 4), 1000),
                    ((i, j, (k + 1) % 4), 1000),
                ]
                ni, nj = add_coord((i, j), direction)
                if input_lines[ni][nj] != '#':
                    result[(i, j, k)].append(
                        ((ni, nj, k), 1)
                    )
                if el == 'E':
                    result[(i, j, k)].append(((i, j), 0))
    return result, start, end


def get_shortest_path_tiles(dist_graph, start, end):
    shortest_paths = dijkstra_all_paths(dist_graph, start)
    end_len, end_paths = shortest_paths[end]
    sp_tiles = set()
    for end_path in end_paths:
        # carefully unpacking since end coordinate has different type :upside-down-face:
        sp_tiles.update([(el_tup[0], el_tup[1]) for el_tup in end_path])
    print(len(sp_tiles))


def main():
    raw_map = TEST_INPUT1.splitlines()
    with open('input/day16.txt') as f:
        raw_map = f.readlines()
    dist_graph, start, end = read_dist_graph(raw_map)
    distance = dijkstra(dist_graph, start)
    print(distance[end])
    get_shortest_path_tiles(dist_graph, start, end)



if __name__ == '__main__':
    main()
