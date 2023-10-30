"""
Arithmetic prompt and answer handling.
"""

import random


def generate_arithmetic(mode: str) -> (str, float):
    """
    Generate a random arithmetic problem that ensures the answer to the random
    problem is an integer. This function returns a tuple whose first value is
    the string representation of the simple arithmetic problem, and whose
    second value is the numeric solution to the problem, which should be used
    to check the user input against.

    A previous iteration of this module provided a separate function for
    actually solving the arithmetic problems generated by this function, but
    for our purposes, we only need the display string for the equation and its
    solution.
    """
    if mode.lower() == "easy":
        sign = {0: "+", 1: "-"}
    elif mode.lower() == "medium" or mode.lower() == "hard":
        sign = {0: "+", 1: "-", 2: "*", 3: "/"}
    else:
        raise AssertionError(f"Difficulty option not valid.")
    random_sign = sign[random.randint(0, 3)]
    random_num_arth1 = random.randint(0, 10)
    random_num_arth2 = random.randint(0, 10)
    if mode.lower() == "hard":
        random_num_arth1 = random.randint(-10, 10)
        random_num_arth2 = random.randint(-10, 10)
    while random_sign == "/":
        while random_num_arth2 == 0:
            if mode.lower() == "hard":
                random_num_arth2 = random.randint(-10, 10)
                continue
            random_num_arth2 = random.randint(0, 10)
        if random_num_arth1 % random_num_arth2 == 0:
            break
        if mode.lower() == "hard":
            random_num_arth1 = random.randint(-10, 10)
            random_num_arth2 = random.randint(-10, 10)
            continue
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
        raise AssertionError(
            f"Unknown sign: {random_sign}. This should be impossible.")

    result = (
        f"{random_num_arth1} {random_sign} {random_num_arth2}",
        float(answer)
    )
    return result
