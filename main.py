import random


def generate_arithmetic():
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


equation = generate_arithmetic()


def solve_arithmetic(problem):
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


print(solve_arithmetic(equation))

