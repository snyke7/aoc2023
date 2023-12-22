from typing import Callable
from attr import define

from utils import *


# TAGS:
#sumtype
#classdesign
#graph
#memoization
#annoying


@define
class CstGate:
    value: int
    _signal: int = None

    def get_signal(self, gates) -> int:
        return self.value


@define
class BinaryGate:
    left_input: str
    right_input: str
    operator: Callable[[int, int], int]
    _signal: int = None

    def get_signal(self, gates) -> int:
        if self._signal is not None:
            return self._signal
        left = gates[self.left_input].get_signal(gates) if self.left_input in gates else int(self.left_input)
        right = gates[self.right_input].get_signal(gates) if self.right_input in gates else int(self.right_input)
        self._signal = self.operator(left, right)
        return self._signal


@define
class UnaryGate:
    my_input: str
    operator: Callable[[int], int]
    _signal: int = None

    def get_signal(self, gates) -> int:
        if self._signal is not None:
            return self._signal
        self._signal = self.operator(gates[self.my_input].get_signal(gates))
        return self._signal


def parse_gate(line: str):
    gate, _, name = line.partition(' -> ')
    if ' OR ' in gate:
        left, _, right = gate.partition(' OR ')
        return name, BinaryGate(left, right, lambda i1, i2: i1 | i2)
    elif ' AND ' in gate:
        left, _, right = gate.partition(' AND ')
        return name, BinaryGate(left, right, lambda i1, i2: i1 & i2)
    elif 'NOT ' in gate:
        return name, UnaryGate(gate[len('NOT '):], lambda i: (~i) & 65535)
    elif ' LSHIFT ' in gate:
        my_input, _, shift_r = gate.partition(' LSHIFT ')
        shift = int(shift_r)
        return name, UnaryGate(my_input, lambda i: (i << shift) & 65535)
    elif ' RSHIFT ' in gate:
        my_input, _, shift_r = gate.partition(' RSHIFT ')
        shift = int(shift_r)
        return name, UnaryGate(my_input, lambda i: (i >> shift) & 65535)
    else:
        try:
            return name, CstGate(int(gate))
        except ValueError:  # redirection
            return name, UnaryGate(gate, lambda i: i)


TEST = '''123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i'''


file_lines = file_read_lines('input/day07_input.txt')
gates = dict([parse_gate(line) for line in file_lines])
# print(gates)
part1 = gates['a'].get_signal(gates)
print(part1)
for gate in gates.values():
    gate._signal = None
gates['b'] = CstGate(part1)
print(gates['a'].get_signal(gates))
