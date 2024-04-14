"""Class with """

import random


def generate_input_state() -> list[str]:
    """Must return one of available initial states"""

    state_length = random.randint(1, 20)

    alphabet = ["1"]
    result = [random.choice(alphabet) for i in range(state_length)]
    result = ["/", "S"] + result + ["/"]

    return result


def generate_answer(initial_state: list[str]) -> list[str]:
    """Must simulate program run and return result"""

    # removing / chars
    state = initial_state[1:-1]

    # removing S
    state = state[1:]

    return ["/"] + state + state + ["/"]
