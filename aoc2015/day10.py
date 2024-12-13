TEST_INPUT = '''1321131112'''


def look_and_say_once(input_str):
    result = ''
    i = 0
    while i < len(input_str):
        cur_num = input_str[i]
        cur_length = 0
        while i < len(input_str) and input_str[i] == cur_num:
            cur_length += 1
            i += 1
        result += f'{cur_length}{cur_num}'
    return result


def look_and_say_steps(input_str, amount):
    result = input_str
    for _ in range(amount):
        result = look_and_say_once(result)
    return result


def main():
    test_input = TEST_INPUT
    print(len(look_and_say_steps(test_input,40)))
    print(len(look_and_say_steps(test_input,50)))

if __name__ == '__main__':
    main()
