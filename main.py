import sys
import argparse
from pathlib import Path
from loguru import logger
from src import constants
from src.interpreter import Interpreter
from src.parser import Parser


def main(program_path: Path, state: list[str] | str) -> None:
    """Main function"""

    logger.remove(0)
    logger.add(
        sys.stdout,
        format=constants.LOGGER_FORMAT,
    )

    parser = Parser(verbose=True)
    parser.update_from_file(path=program_path)
    # parser.update_from_file("./examples/is_palindrome.grammar")

    app = Interpreter(verbose=True)
    app.set_state(state=state)
    # app.set_state("/S10011110001111001/")
    app.set_rules(parser.get_rules())
    app.run()


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(
        # prog="grammar",
        description="Interprets subset of grammar 0 programs",
    )

    args_parser.add_argument("program_path", type=str, help="Path to the program file")
    args_parser.add_argument(
        "state", type=str, nargs="*", help="Start state of program"
    )
    args = args_parser.parse_args()

    program_path = Path(args.program_path)
    state = args.state
    if len(state) == 0:
        logger.error("invalid state: check README.md")
        sys.exit(0)

    if len(state) == 1:
        state = list(state[0])

    main(program_path=program_path, state=state)
