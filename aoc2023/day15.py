TEST = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
'''


def compute_hash(the_str):
    result = 0
    for c in the_str:
        result += ord(c)
        result *= 17
        result = result % 256
    return result


def process_step(step, box_map):
    if '=' in step:
        label, _, operation = step.partition('=')
        operation = '=' + operation
    elif '-' in step:
        label = step.partition('-')[0]
        operation = '-'
    else:
        raise ValueError(step)
    box = compute_hash(label)
    if box not in box_map:
        box_map[box] = {}
    if operation == '-':
        if label in box_map[box]:
            del box_map[box][label]
    elif operation.startswith('='):
        focal_length = int(operation[1:])
        box_map[box][label] = focal_length  # always does the right thing
    else:
        raise ValueError(step, 'what happened..?')


def total_focusing_power(box_map):
    result = 0
    for box, lens_dict in box_map.items():
        for i, focal_length in enumerate(lens_dict.values()):
            result += (box + 1) * (i + 1) * focal_length
    return result


def main():
    with open('input/day15_input.txt') as f:
        input_line = f.read().strip()
    input_line2 = TEST.strip()
    steps = input_line.split(',')
    print(sum(map(compute_hash, steps)))
    box_map = {}
    for step in steps:
        process_step(step, box_map)
    print(box_map)
    print(total_focusing_power(box_map))


if __name__ == '__main__':
    main()
