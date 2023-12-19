from typing import List

from attr import define


TEST = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''


def parse_part(part_line):
    interior = part_line.strip()[1:-1]
    return {
        kvpair.partition('=')[0]: int(kvpair.partition('=')[2])
        for kvpair in interior.split(',')
    }


COMMAND_LT = 0
COMMAND_GT = 1
COMMAND_YES = 2


@define
class Command:
    command_type: int
    command_destination: str
    command_cmp: str = ''
    command_info: int = 0

    def __repr__(self):
        if self.command_type == COMMAND_LT:
            return f'Cmd({self.command_cmp}<{self.command_info}:{self.command_destination})'
        elif self.command_type == COMMAND_GT:
            return f'Cmd({self.command_cmp}>{self.command_info}:{self.command_destination})'
        elif self.command_type == COMMAND_YES:
            return f'Cmd({self.command_destination})'
        else:
            raise f'Cmd(UNKNOWN)'

    def get_destination(self, part):
        if self.command_type == COMMAND_YES:
            return self.command_destination
        the_val = part[self.command_cmp]
        if self.command_type == COMMAND_LT:
            if the_val < self.command_info:
                return self.command_destination
        elif self.command_type == COMMAND_GT:
            if the_val > self.command_info:
                return self.command_destination
        return None

    def get_destination_ranges(self, part_range):
        if self.command_type == COMMAND_YES:
            return [(self.command_destination, part_range)]
        lb, ub = part_range[self.command_cmp]
        if self.command_type == COMMAND_LT:
            if lb < self.command_info:
                if ub <= self.command_info:
                    return [(self.command_destination, part_range)]
                # otherwise, we have to split
                range_l = part_range.copy()
                range_r = part_range.copy()
                range_l[self.command_cmp] = lb, self.command_info
                range_r[self.command_cmp] = self.command_info, ub
                return [
                    (self.command_destination, range_l),
                    (None, range_r)
                ]
        elif self.command_type == COMMAND_GT:
            if ub - 1 > self.command_info:
                if lb > self.command_info:
                    return [(self.command_destination, part_range)]
                # otherwise, we have to split
                range_l = part_range.copy()
                range_r = part_range.copy()
                range_l[self.command_cmp] = lb, self.command_info + 1
                range_r[self.command_cmp] = self.command_info + 1, ub
                return [
                    (None, range_l),
                    (self.command_destination, range_r)
                ]
        return [(None, part_range)]


@define
class Workflow:
    commands: List[Command]

    def get_destination_ranges(self, part_range):
        results = []
        to_process = [(0, part_range)]
        while to_process:
            cmd_i, this_range = to_process.pop()
            result = self.commands[cmd_i].get_destination_ranges(this_range)
            for dest, result_range in result:
                if dest is None:
                    to_process.append((cmd_i + 1, result_range))
                else:
                    results.append((dest, result_range))
        return results


def parse_command(command_str):
    if ':' not in command_str:
        return Command(COMMAND_YES, command_str)
    condition, _, dest = command_str.partition(':')
    cmp = condition[0]
    info = int(condition[2:])
    if condition[1] == '<':
        return Command(COMMAND_LT, dest, cmp, info)
    elif condition[1] == '>':
        return Command(COMMAND_GT, dest, cmp, info)
    else:
        raise ValueError(command_str)


def parse_workflow(workflow_line):
    label, _, workflow_descr = workflow_line.strip()[:-1].partition('{')
    commands = [parse_command(cmd) for cmd in workflow_descr.split(',')]
    return label, Workflow(commands)


def process_part(part, workflows):
    cur_flow = workflows['in']
    while True:
        for cmd in cur_flow.commands:
            dest = cmd.get_destination(part)
            if dest is not None:
                if dest == 'A':
                    return True
                elif dest == 'R':
                    return False
                else:
                    cur_flow = workflows[dest]
                    break


def process_part_ranges(part_range, workflows):
    results = []
    to_process = [('in', part_range)]
    while to_process:
        workflow_label, this_range = to_process.pop()
        workflow = workflows[workflow_label]
        result = workflow.get_destination_ranges(this_range)
        # print(f'{workflow}\n mapped {this_range} to\n {result}\n\n')
        for dest, result_range in result:
            if dest == 'A':
                results.append(result_range)
            elif dest == 'R':
                pass  # drop it
            else:
                to_process.append((dest, result_range))
    return results


def count_combinations(part_range):
    result = 1
    for lb, ub in part_range.values():
        result *= (ub - lb)
    return result


def main():
    with open('input/day19_input.txt') as f:
        raw_input = f.read()
    raw_input2 = TEST
    raw_workflows, _, raw_parts = raw_input.partition('\n\n')
    parts = [parse_part(part) for part in raw_parts.splitlines()]
    workflows = dict([parse_workflow(line) for line in raw_workflows.splitlines()])
    accepted_parts = [part for part in parts if process_part(part, workflows)]
    print(sum((sum(part.values()) for part in accepted_parts)))

    result_ranges = process_part_ranges({
        'x': (1, 4001),
        'm': (1, 4001),
        'a': (1, 4001),
        's': (1, 4001),
    }, workflows)
    print(sum((count_combinations(the_range) for the_range in result_ranges)))


if __name__ == '__main__':
    main()
