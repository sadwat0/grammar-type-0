"""Class with """

import random


def generate_input_state() -> list[str]:
    """Must return one of available initial states"""

    state_length = random.randint(1, 20)

    alphabet = ["0", "1"]
    result = [random.choice(alphabet) for i in range(state_length)]
    result = ["/", "S"] + result + ["/"]

    return result


def generate_answer(initial_state: list[str]) -> list[str]:
    """Must simulate program run and return result"""

    # removing / chars
    state = initial_state[1:-1]

    # removing S and reversing
    state = state[1:]
    state = state[::-1]

    # adding 1
    carry = True
    for i, character in enumerate(state):
        if character == "0":
            state[i] = "1"
            carry = False
            break

        state[i] = "0"

    if carry:
        state += ["1"]

    # reversing back
    state = state[::-1]

    return ["/"] + state + ["/"]
