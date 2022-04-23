from random import choice

all_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate_code():
    code = ""
    for i in range(25):
        code += choice(all_chars)
    return code