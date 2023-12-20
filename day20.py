from typing import List, Any, Dict, Tuple

from attr import define

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
    received_pulses: List[bool] = []

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
                print(f'Inserting output node for label: {dest}')
                node_dict[dest] = OutputNode()
            if isinstance(node_dict[dest], NandNode):
                node_dict[dest].prev_inputs[label] = False
    return node_dict


def button_push(node_dict):
    pulses_to_process = [('broadcaster', False, 'button')]
    low_count = 0
    high_count = 0
    while pulses_to_process:
        dest, is_high, src = pulses_to_process.pop(0)
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


def button_repeat_until_output(node_dict):
    pushes = 0
    output = node_dict['rx']
    while True:
        button_push(node_dict)
        if pushes % 100000 == 99999:
            print(pushes, output.received_pulses)
        if False in output.received_pulses:
            print(f'Encountered a low pulse! {pushes} {output.received_pulses}')
            return pushes
        if output.received_pulses == [False]:
            return pushes
        pushes += 1
        output.received_pulses = []


def main():
    with open('input/day20_input.txt') as f:
        input_lines = f.readlines()
    input_lines2 = TEST2.splitlines()
    node_dict = parse_nodes(input_lines)
    # print(node_dict)
    print(button_mash(node_dict))
    print(button_repeat_until_output(node_dict))


if __name__ == '__main__':
    main()
