TEST_INPUT = 'hxbxwxba'


DIGIT_MAP = dict(enumerate(
    chr(97 + i)
    for i in range(26)
    if chr(97 + i) not in 'ilo'
))

REV_DIGIT_MAP = {
    v: k
    for k, v in DIGIT_MAP.items()
}


def pwd_to_str(pwd_num, pwd_len):
    the_bit = pwd_len - 1
    result = ''
    while the_bit >= 0:
        digit = pwd_num // (23 ** the_bit)
        result += DIGIT_MAP[digit]
        pwd_num -= digit * 23 ** the_bit
        the_bit -= 1
    return result


def pwd_of_str(pwd_str):
    return sum((
        REV_DIGIT_MAP[c] * 23 ** (len(pwd_str) - 1 - idx)
        for idx, c in enumerate(pwd_str)
    ))


def criteria1(pwd_str):
    alphabet = ''.join((chr(97 + i) for i in range(26)))
    return any((
        alphabet[i:i+3] in pwd_str
        for i in range(26 - 3 + 1)
    ))


def criteria3(pwd_str):
    return sum((
        1
        for i in range(26)
        if chr(97 + i) * 2 in pwd_str
    )) >= 2


def test_pwd(pwd_str):
    return criteria1(pwd_str) and criteria3(pwd_str)


def get_next_good_password(pwd_str):
    pwd_num = pwd_of_str(pwd_str)
    pwd_len = len(pwd_str)
    pwd_num += 1
    pwd_str = pwd_to_str(pwd_num, pwd_len)
    while not test_pwd(pwd_str):
        pwd_num += 1
        pwd_str = pwd_to_str(pwd_num, pwd_len)
    return pwd_str


def main():
    test_input = TEST_INPUT
    print(criteria1('hijklmmn'))
    print(criteria3('abbceffg'))
    print(criteria1('abbceffg'))
    print(criteria3('abbcegjk'))
    print(get_next_good_password('abcdefgh'))
    print(get_next_good_password('ghjaaaaa'))
    result1 = get_next_good_password(test_input)
    print(result1)
    print(get_next_good_password(result1))


if __name__ == '__main__':
    main()
