from utils import *
from hashlib import md5 as md5_base


# TAGS:
#trivial


def md5(the_str: str):
    md5_obj = md5_base(the_str.encode('utf-8'))
    return md5_obj.hexdigest()


the_input = 'iwrupvqb'
i = 0
while not md5(f'{the_input}{i}').startswith('000000'):
    i += 1
print(i)
