from typing import List, Any, Dict, Tuple
from day08 import lcm

from attr import define, Factory

TEST1 = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

TEST2 = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''


@define
class FlipFlopNode:
    destinations: List[str]
    is_on: bool = False

    def receive_pulse(self, from_label: str, is_high: bool) -> List[Tuple[str, bool]]:
        if is_high:
            return []
        self.is_on = not self.is_on
        return [(dest, self.is_on) for dest in self.destinations]


@define
class NandNode:
    destinations: List[str]
    prev_inputs: Dict[str, bool]

    def receive_pulse(self, from_label: str, is_high: bool) -> List[Tuple[str, bool]]:
        self.prev_inputs[from_label] = is_high
        send_is_high = not all((was_high for was_high in self.prev_inputs.values()))
        return [(dest, send_is_high) for dest in self.destinations]


@define
class BroadcastNode:
    destinations: List[str]

    def receive_pulse(self, from_label, is_high: bool) -> List[Tuple[str, bool]]:
        return [(dest, is_high) for dest in self.destinations]


@define
class OutputNode:
    received_pulses: List[bool] = Factory(list)
    destinations: List[str] = Factory(list)

    def receive_pulse(self, from_label: str, is_high: bool) -> List[Tuple[str, bool]]:
        self.received_pulses.append(is_high)
        return []


def parse_node(input_line):
    raw_node, _, raw_dests = input_line.partition(' -> ')
    dests = raw_dests.split(', ')
    if raw_node == 'broadcaster':
        return raw_node, BroadcastNode(dests)
    elif raw_node.startswith('%'):
        return raw_node[1:], FlipFlopNode(dests)
    elif raw_node.startswith('&'):
        return raw_node[1:], NandNode(dests, {})  # will be initialized later
    else:
        raise ValueError(input_line)


def parse_nodes(input_lines):
    node_dict = dict([parse_node(line.strip()) for line in input_lines])
    for label, node in list(node_dict.items()):
        for dest in node.destinations:
            if dest not in node_dict:
                node_dict[dest] = OutputNode()
            if isinstance(node_dict[dest], NandNode):
                node_dict[dest].prev_inputs[label] = False
    return node_dict


def button_push(node_dict, verbose=False):
    pulses_to_process = [('broadcaster', False, 'button')]
    low_count = 0
    high_count = 0
    while pulses_to_process:
        dest, is_high, src = pulses_to_process.pop(0)
        if verbose:
            print(f'{src} -{"high" if is_high else "low"}> {dest}')
        if is_high:
            high_count += 1
        else:
            low_count += 1
        new_pulses = node_dict[dest].receive_pulse(src, is_high)
        pulses_to_process.extend(((new_dest, new_high, dest) for new_dest, new_high in new_pulses))
    return low_count, high_count


def button_mash(node_dict):
    result_low = 0
    result_high = 0
    for i in range(1000):
        low, high = button_push(node_dict)
        result_low += low
        result_high += high
    return result_low * result_high


def button_repeat_until_output(node_dict, output_label='rx'):
    pushes = 0
    output = node_dict[output_label]
    while True:
        button_push(node_dict)
        pushes += 1
        if pushes % 100000 == 99999:
            print(pushes, output.received_pulses)
        if False in output.received_pulses:
            print(f'Encountered a low pulse! {pushes} {output.received_pulses}')
            return pushes
        if output.received_pulses == [False]:
            return pushes
        output.received_pulses = []


def get_reachable_nodes(node_dict, start_nodes):
    # reachable, but skipping internal connections
    result = set()
    to_process = list(start_nodes)
    while to_process:
        node = to_process.pop()
        for dest in node_dict[node].destinations:
            if dest not in result and not (node in start_nodes and dest in start_nodes):
                result.add(dest)
                to_process.append(dest)
    return result


def find_sub_circuit(node_dict, start_node):
    cur_circuit = [start_node]
    while get_reachable_nodes(node_dict, cur_circuit).intersection(cur_circuit):
        for node in cur_circuit:
            for dest in node_dict[node].destinations:
                if dest not in cur_circuit:
                    that_reach = get_reachable_nodes(node_dict, [dest])
                    if that_reach.intersection(cur_circuit):
                        cur_circuit.append(dest)
                        break
    return cur_circuit


def get_state(node_dict):
    return frozenset({
        (label, node.is_on)
        for label, node in node_dict.items()
        if isinstance(node, FlipFlopNode)
    })


def reset(node_dict):
    for _, node in node_dict.items():
        if isinstance(node, FlipFlopNode):
            node.is_on = False


def compute_pattern_atomic(node_dict, output_label, verbose=False):
    reset(node_dict)
    cur_state = get_state(node_dict)
    pushes = 0
    state_index = {cur_state: pushes}
    output = node_dict[output_label]
    output.received_pulses = []  # to be sure
    while True:
        button_push(node_dict, verbose=verbose)
        if verbose:
            print()
        pushes += 1
        if False in output.received_pulses and verbose:
            print(f'Encountered False after {pushes} pushes')
        node_dict[output_label].received_pulses = []
        cur_state = get_state(node_dict)
        if cur_state in state_index:
            print(f'Detected cycle: after {pushes} we jump back to state index {state_index[cur_state]}')
            if pushes < 100:
                print(cur_state)
            break
        state_index[cur_state] = pushes
    return state_index, pushes


def compute_pattern(node_dict):
    sub_circuits = {label: find_sub_circuit(node_dict, label) for label in node_dict['broadcaster'].destinations}
    false_cycles = {}
    for label, sub_circuit in sub_circuits.items():
        sub_node_dict = {label: node for label, node in node_dict.items() if label in sub_circuit}
        sub_node_dict['broadcaster'] = BroadcastNode([label])
        output = list(get_reachable_nodes(node_dict, sub_circuit).difference({'kl', 'rx'}))[0]  # yeah, hardcoded..
        sub_node_dict[output] = OutputNode()
        state_index, pulses = compute_pattern_atomic(sub_node_dict, output)
        # apparently, we do not need to get tricky: first False == last push of cycle, which always jumps back to 0
        false_cycles[label] = pulses
    return lcm_multi(list(false_cycles.values()))


def lcm_multi(els):
    if len(els) == 1:
        return els[0]
    else:
        return lcm(els[0], lcm_multi(els[1:]))


TEST3 = '''broadcaster -> in
%in -> middle, inv
%middle -> inv
&inv -> out'''

TEST4 = '''broadcaster -> middle1
%middle1 -> middle2, inv
%middle2 -> middle3, inv
%middle3 -> inv, middle4
%middle4 -> middle5
%middle5 -> middle6
%middle6 -> inv, middle7
%middle7 -> middle8
%middle8 -> inv, middle9
%middle9 -> inv, middle10
%middle10 -> middle11, inv
%middle11 -> middle12, inv
%middle12 -> inv
&inv -> middle7, middle5, middle4, middle1, out'''

TEST5 = '''broadcaster -> middle1
%middle1 -> middle2, inv
%middle2 -> middle4, inv
%middle4 -> middle5, inv
%middle5 -> inv
&inv -> middle1, out'''


def main():
    with open('input/day20_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST2.splitlines()
    node_dict = parse_nodes(input_lines)
    # print(node_dict)
    print(button_mash(node_dict))
    reset(node_dict)
    # print(button_repeat_until_output(node_dict))
    assert compute_pattern_atomic(parse_nodes(input_lines2), 'output')[1] == 4

    print(compute_pattern(node_dict))

    node_dict3 = parse_nodes(TEST5.splitlines())
    print(compute_pattern_atomic(node_dict3, 'out', True)[1])


if __name__ == '__main__':
    main()
