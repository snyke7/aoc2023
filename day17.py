from typing import Dict, List, Tuple

from utils import dijkstra


Coord = Tuple[int, int, bool]  # bool indicates arrived_horizontal


TEST = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''


TEST2 = '''111111111111
999999999991
999999999991
999999999991
999999999991'''


def parse_graph(input_lines, min_steps=1, max_steps=3) -> Dict[Coord, List[Tuple[Coord, int]]]:
    result = {}
    for i, line in enumerate(input_lines):
        for j in range(len(line.strip())):
            result[(i, j, False)] = []

            sum_dist = 0
            for n in range(1, max_steps + 1):
                if j - n < 0:
                    break
                sum_dist += int(input_lines[i][j - n])
                if n >= min_steps:
                    result[(i, j, False)].append(((i, j - n, True), sum_dist))

            sum_dist = 0
            for n in range(1, max_steps + 1):
                if j + n >= len(input_lines[i].strip()):
                    break
                sum_dist += int(input_lines[i][j + n])
                if n >= min_steps:
                    result[(i, j, False)].append(((i, j + n, True), sum_dist))

            result[(i, j, True)] = []

            sum_dist = 0
            for n in range(1, max_steps + 1):
                if i - n < 0:
                    break
                sum_dist += int(input_lines[i - n][j])
                if n >= min_steps:
                    result[(i, j, True)].append(((i - n, j, False), sum_dist))

            sum_dist = 0
            for n in range(1, max_steps + 1):
                if i + n >= len(input_lines):
                    break
                sum_dist += int(input_lines[i + n][j])
                if n >= min_steps:
                    result[(i, j, True)].append(((i + n, j, False), sum_dist))
    return result


def main():
    with open('input/day17_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST.splitlines()
    start_down = (0, 0, True)
    start_right = (0, 0, False)
    end_arrive_down = (len(input_lines) - 1, len(input_lines[-1].strip()) - 1, False)
    end_arrive_right = (len(input_lines) - 1, len(input_lines[-1].strip()) - 1, True)

    # part 1
    graph = parse_graph(input_lines)
    distances_down = dijkstra(graph, start_down)
    distances_right = dijkstra(graph, start_right)
    print(min(
        distances_down[end_arrive_down],
        distances_down[end_arrive_right],
        distances_right[end_arrive_right],
        distances_right[end_arrive_down]
    ))

    # part 2
    graph = parse_graph(input_lines, 4, 10)
    distances_down = dijkstra(graph, start_down)
    distances_right = dijkstra(graph, start_right)
    print(min(
        distances_down[end_arrive_down],
        distances_down[end_arrive_right],
        distances_right[end_arrive_right],
        distances_right[end_arrive_down]
    ))


if __name__ == '__main__':
    main()
