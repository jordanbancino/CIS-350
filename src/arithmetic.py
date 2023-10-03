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

    return [f"{random_num_arth1} {random_sign} {random_num_arth2}", random_num_arth1, random_sign, random_num_arth2]


def solve_arithmetic(problem: list) -> bool:
    """
    The function solve_arithmetic is a function that allows the player to input an answer to the arithmetic problem
    and checks if it is right or wrong.
    problem is a list in the format: [(printable arithmetic function), first num of arithmetic problem, arithmetic
    sign (+, -, *, /), second num of arithmetic problem] that serves as the printable random arithmetic problem
    and contains the equation that is used to check the player's answer.
    The function returns a boolean that represents if the answer to the problem is right or wrong.  True is correct
    and False is incorrect.
    """
    print(problem[0])
    answer = 0
    if problem[2] == "+":
        answer = int(problem[1] + problem[3])
    elif problem[2] == "-":
        answer = int(problem[1] - problem[3])
    elif problem[2] == "*":
        answer = int(problem[1] * problem[3])
    elif problem[2] == "-":
        answer = int(problem[1] / problem[3])
    print(answer)
    user_input = input("Please enter an integer that solves the problem: ")
    while not user_input.isdigit():
        user_input = input("Please enter an integer that solves the problem: ")
    if int(user_input) != answer:
        return False
    return True
