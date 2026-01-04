SUE_PROPS = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
'''


def into_sue_dict(sue_prop_list):
    sue_props = {}
    for kv in sue_prop_list:
        key, _, value = kv.partition(': ')
        sue_props[key] = int(value)
    return sue_props


def parse_sue_line(sue_line):
    sue_num, _, sue_props_str = sue_line[len('Sue '):].partition(': ')
    return int(sue_num), into_sue_dict(sue_props_str.split(', '))


def check_matches_pt2(key, mfcsam_val, actual_val):
    if key in {'cats', 'trees'}:
        return actual_val < mfcsam_val
    elif key in {'pomeranians', 'goldfish'}:
        return actual_val > mfcsam_val
    else:
        return mfcsam_val == actual_val


def main():
    with open('input/day16.txt') as f:
        sue_list_raw =  f.read()
    sues = dict((parse_sue_line(line) for line in sue_list_raw.splitlines()))
    real_sue_props = into_sue_dict(SUE_PROPS.splitlines())
    for sue_num, sue_props in sues.items():
        matches = all((
            real_sue_props[key] == val
            for key, val in sue_props.items()
        ))
        if matches:
            print(f'Pt1 could be {sue_num}')

    for sue_num, sue_props in sues.items():
        matches = all((
            check_matches_pt2(key, val, real_sue_props[key])
            for key, val in sue_props.items()
        ))
        if matches:
            print(f'Pt2 could be {sue_num}')



if __name__ == '__main__':
    main()
