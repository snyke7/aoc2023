TEST_INPUT = '''e => H
e => O
H => HO
H => OH
O => HH
'''


def parse_replacements(test_input):
    return [tuple(list(line.partition(' => '))[::2]) for line in test_input.splitlines()]


def mutate_with_reps(base, replacements):
    result = set()
    for to_rep, rep_with in replacements:
        start_idx = 0
        while to_rep in base[start_idx:]:
            occ_idx = base.index(to_rep, start_idx)
            to_add = base[:occ_idx] + rep_with + base[occ_idx + len(to_rep):]
            result.add(to_add)
            start_idx = occ_idx + 1
    return result


def parse_input(input_str):
    rep_str, _, base = input_str.partition('\n\n')
    return base.strip(), parse_replacements(rep_str)


def find_shortest_path_to(reps, dest):
    result = {'e': 0}
    new_els = ['e']
    while new_els:
        el = new_els.pop(0)
        num_reps = result[el]
        for rep in mutate_with_reps(el, reps):
            if len(rep) > len(dest):
                continue
            if rep in result and result[rep] <= num_reps + 1:
                continue
            result[rep] = num_reps + 1
            new_els.append(rep)
    return result[dest]


def find_shortest_path_back(reps, dest):
    result = {dest: 0}
    new_els = [dest]
    reps_back = [(rep_with, to_rep) for to_rep, rep_with in reps]
    while new_els:
        el = new_els.pop(0)
        num_reps = result[el]
        for rep in mutate_with_reps(el, reps_back):
            if len(rep) > len(dest):
                continue
            if rep in result and result[rep] <= num_reps + 1:
                continue
            if 'e' in rep and rep != 'e':
                continue
            result[rep] = num_reps + 1
            new_els.append(rep)
            if len(result) % 10000 == 0:
                print(len(new_els), len(result), len(rep), rep)
    return result['e']


def head_transforms(base, reps_back):
    # the first character of base must be the result of the last replacement of the previous character.
    # for this to have happened, the subsequent characters must be back-translatable to something which matches
    # that translation on the first character
    # base case:
    print(base[:50])
    yield base, 0

    for to_rep, rep_with in reps_back:
        if base[0] != to_rep[0]:
            continue
        # now transform the next character
        for i in range(1, len(to_rep)):
            for second_transf, num_reps in head_transforms(base[i:], reps_back):
                if second_transf[:len(to_rep) - i] == to_rep[i:]:
                    yield rep_with + second_transf[len(to_rep) - i], num_reps + 1


# ORnPBPMgArCaCaCaSiThCaC
# H => ORnFAr
# PBPMgAr =??=> FAr
# PB => Ca
# PRnFAr => Ca
# PMg => F
# PTi => P

# BPMgr =??=> B
# BCa => B
# BF => Mg
# BP => Ti


def is_boxing_rep(rep):
    # reps of the form ..Rn...Ar
    return 'Rn' in rep


def into_elements(rep):
    result = []
    cur_el = rep[0]
    for c in rep[1:]:
        if c.isupper():
            result.append(cur_el)
            cur_el = c
        else:
            cur_el += c
    result.append(cur_el)
    return result


def main():
    base, test_input = 'HOH', TEST_INPUT
    reps = parse_replacements(test_input)
    print(len(mutate_with_reps(base, reps)))
    print(find_shortest_path_to(reps, 'HOH'))
    print(find_shortest_path_back(reps, 'HOH'))
    print(find_shortest_path_to(reps, 'HOHOHO'))
    print(find_shortest_path_back(reps, 'HOHOHO'))

    with open('input/day19.txt') as f:
        base, reps = parse_input(f.read())
    print(len(mutate_with_reps(base, reps)))
    reps_back = [(rep_with, to_rep) for to_rep, rep_with in reps]
    box_reps = [(rep, rep_with) for rep, rep_with in reps_back if is_boxing_rep(rep)]
    non_box_reps = [(rep, rep_with) for rep, rep_with in reps_back if not is_boxing_rep(rep)]

    # how we get rid of non_box_reps is not relevant: each transforms two elements into 1
    assert(all((len(into_elements(rep)) == 2 for rep, _ in non_box_reps)))
    assert(all((len(into_elements(rep_with)) == 1 for _, rep_with in non_box_reps)))

    # therefore, the main challenge is to get rid of box_reps. each of these contains an 'Rn' element, and ends
    # with an 'Ar' element
    assert(all((rep[-2:] == 'Ar' for rep, _ in box_reps)))
    assert(all(('Rn' in rep for rep, _ in box_reps)))

    # moreover, these two elements, as well as 'Y', are not creatable via non_box_reps
    assert(all(('Rn' not in rep and 'Ar' not in rep and 'Y' not in rep for rep, _ in non_box_reps)))

    # this means that when we have a destination molecule <start>Rn<plain>Ar
    # where Ar and Rn not in <plain>, then <plain> must be created only via non-box replacements.
    # and non-box replacements always add/delete one molecule
    print(box_reps)

    # furthermore, all box_reps have length 4 + 2 * (number of Ys in rep)
    assert(all((len(into_elements(rep)) == 4 + 2 * rep.count('Y') for rep, _ in box_reps)))
    # remember that Ys are only created via box_reps. Thus, independent of which box_rep we use, the number of Ys
    # always dictates the resulting length, thus the number of required steps

    # given these assumptions, we can calculate the number of replacements as follows
    element_list = into_elements(base)
    print(calculate_num_replacements(element_list))


def calculate_num_replacements(el_list):
    num_reps = 0
    is_boxing = False
    boxing_start = -1
    boxing_depth = 0
    for i, el in list(enumerate(el_list))[1:]:
        if not is_boxing:
            if el == 'Y':
                num_reps -= 1
                continue
            if el != 'Rn':
                num_reps += 1
                continue
            is_boxing = True
            boxing_start = i + 1
            boxing_depth = 1
        else:
            if el == 'Rn':
                boxing_depth += 1
            elif el == 'Ar':
                boxing_depth -= 1
            if boxing_depth == 0:
                # exit box
                box_content = el_list[boxing_start:i]
                replacements_for_box_content = calculate_num_replacements(box_content)
                num_reps += replacements_for_box_content + 1  # one additional to get rid of the box itself
                is_boxing = False
    return num_reps


if __name__ == '__main__':
    main()
