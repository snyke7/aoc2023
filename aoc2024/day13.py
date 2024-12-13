from typing import Tuple, Optional

from attr import define

TEST_INPUT = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''


@define
class Machine:
    move_a: Tuple[int, int]
    move_b: Tuple[int, int]
    dest: Tuple[int, int]

    def get_required_presses(self) -> Optional[Tuple[int, int]]:
        if are_colinear(self.move_a, self.move_b):
            print(f'{self} has colinear moves!')
            return None
        # solve the 2x2 matrix:
        # [a[0] b[0]]   [pa]   [d[0]]
        # [a[1] b[1]] * [pb] = [d[1]]
        # -----------------
        # inverse matrix:
        # [b[1] -b[0]]
        # [-a[1] a[0]] * (1/(b[1]*a[0] -b[0]*a[1]))
        determinant = self.move_b[1] * self.move_a[0] - self.move_b[0] * self.move_a[1]
        pa_mult = self.move_b[1] * self.dest[0] - self.move_b[0] * self.dest[1]
        pb_mult = -self.move_a[1] * self.dest[0] + self.move_a[0] * self.dest[1]
        if pa_mult % determinant != 0:
            return None
        if pb_mult % determinant != 0:
            return None
        return pa_mult // determinant, pb_mult // determinant

    def get_minimum_win_cost(self):
        maybe_presses = self.get_required_presses()
        if maybe_presses is None:
            return 0
        pa, pb = maybe_presses
        return 3 * pa + pb

    def add_pt2_conversion_error(self):
        self.dest = self.dest[0] + 10000000000000, self.dest[1] + 10000000000000


def read_coord(coord_str, sep):
    return int(coord_str.partition(sep)[2])


def read_coords(coords_str, sep):
    x_str, y_str = tuple(coords_str.split(', '))
    return read_coord(x_str, sep), read_coord(y_str, sep)


def read_move(move_str):
    return read_coords(move_str, '+')


def read_dest(dest_str):
    return read_coords(dest_str, '=')


def read_machine(machine_str):
    a_str, b_str, prize_str = tuple(machine_str.split('\n'))
    return Machine(read_move(a_str), read_move(b_str), read_dest(prize_str))


def are_colinear(vec1: Tuple[int, int], vec2: Tuple[int, int]):
    return (vec1[0] * vec2[1] - vec1[1] * vec2[0]) == 0


def main():
    test_input = TEST_INPUT
    with open('input/day13.txt') as f:
        test_input = f.read()
    machine_configs = [read_machine(machine.strip()) for machine in test_input.split('\n\n')]
    print(sum([machine.get_minimum_win_cost() for machine in machine_configs]))
    for machine in machine_configs:
        machine.add_pt2_conversion_error()
    print(sum([machine.get_minimum_win_cost() for machine in machine_configs]))


if __name__ == '__main__':
    main()
