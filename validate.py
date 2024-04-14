"""Validates your grammar 0 program using python checker and generator"""

import sys
import argparse
import importlib.machinery
from pathlib import Path
from loguru import logger
from src import constants
from src.interpreter import Interpreter
from src.parser import Parser
from src import utils


def load_module_from_path(path: Path | str):
    """Loads validator from given path"""

    print(path)
    spec = importlib.util.spec_from_file_location("validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_test(parser: Parser, state: list[str] | str) -> bool:
    """Runs one test"""

    app = Interpreter(verbose=False)
    app.set_rules(parser.get_rules())
    app.set_state(state=state)

    app.run()

    final_state = app.state

    return final_state


if __name__ == "__main__":
    logger.remove(0)
    logger.add(
        sys.stdout,
        format=constants.LOGGER_FORMAT,
    )

    args_parser = argparse.ArgumentParser(
        # prog="grammar",
        description="Interprets subset of grammar 0 programs",
    )

    args_parser.add_argument("program_path", type=str, help="Path to the program file")
    args_parser.add_argument("validator_path", type=str, help="Path to validator")
    args_parser.add_argument(
        "-c",
        "--count",
        dest="count",
        type=int,
        default=100,
        help="Count of tests to check",
    )
    args_parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        # type=bool,
        type=str,
        default="True",
        help="Verbose option",
    )

    args = args_parser.parse_args()

    program_path = Path(args.program_path)
    validator_path = Path(args.validator_path)
    tests_count = args.count

    verbose = args.verbose
    verbose = True if verbose.lower() == "true" else False

    validator_library = load_module_from_path(path=validator_path)

    parser = Parser(verbose=verbose)
    parser.update_from_file(path=program_path)

    logger.info("Started testing.")

    for test_idx in range(tests_count):
        initial_state = validator_library.generate_input_state()
        generated_answer = run_test(parser=parser, state=initial_state)
        correct_answer = validator_library.generate_answer(initial_state)

        if generated_answer == correct_answer and verbose:
            logger.success(f"Test #{test_idx + 1} passed.")

        if generated_answer != correct_answer:
            logger.error(f"Test #{test_idx + 1} failed.")

            logger.info(
                "Initial state: "
                f"{utils.state_to_string(state=initial_state, divider=parser.divider)}"
            )
            logger.info(
                "Correct answer: "
                f"{utils.state_to_string(state=correct_answer, divider=parser.divider)}"
            )
            logger.info(
                "Generated answer: "
                f"{utils.state_to_string(state=generated_answer, divider=parser.divider)}"
            )

            sys.exit(1)

    logger.success(
        "Passed all tests. You can try to increase tests count using --count option."
    )
