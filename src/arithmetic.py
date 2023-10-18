"""
arithmetic module: arithmetic prompt and answer handling
"""

import random


def generate_arithmetic() -> list:
    """
    The function generate_arithmetic is a function that is designed to make a random arithmetic problem that ensures
    the answer to the random problem is an integer.
    The function returns a list of length 4 that is in the format: [(printable arithmetic function), first num of
    arithmetic problem, arithmetic sign (+, -, *, /), second num of arithmetic problem]
    """
    sign = {0: "+", 1: "-", 2: "*", 3: "/"}
    random_sign = sign[random.randint(0, 3)]
    random_num_arth1 = random.randint(0, 10)
    random_num_arth2 = random.randint(0, 10)
    while random_sign == "/":
        while random_num_arth2 == 0:
            random_num_arth2 = random.randint(0, 100)
        if random_num_arth1 % random_num_arth2 == 0:
            break
        random_num_arth1 = random.randint(0, 10)
        random_num_arth2 = random.randint(0, 10)

    if random_sign == '+':
        answer = random_num_arth1 + random_num_arth2
    elif random_sign == '-':
        answer = random_num_arth1 - random_num_arth2
    elif random_sign == '*':
        answer = random_num_arth1 * random_num_arth2
    elif random_sign == '/':
        answer = random_num_arth1 / random_num_arth2
    else:
        raise AssertionError(f"Unknown sign: {random_sign}. This should be impossible.")

    result = [f"{random_num_arth1} {random_sign} {random_num_arth2}", str(answer)]
    return result
