__author__ = 'Yuxiang'

from random import choice

def generate_code():
    """
    生成4位验证码
    :return:
    """
    seeds = '1234567890'
    random_str = []
    for i in range(4):
        random_str.append(choice(seeds))
    return ''.join(random_str)
