from loguru import logger
import sys
from src import constants
from src.interpreter import Interpreter
from src.rule import Rule
from src.parser import Parser


logger.remove(0)
logger.add(
    sys.stdout,
    format=constants.LOGGER_FORMAT,
)


parser = Parser(verbose=True)
parser.update_from_file("./examples/is_palindrome.grammar")

app = Interpreter()
app.set_state("/S10011110001111001/")
app.set_rules(parser.get_rules())
app.run()

# TODO: add arguments parsing, change main.py

# app.set_rules(
#     [
#         ("S1", "2R"),
#         ("R1", "1R"),
#         ("R/", "L2/"),
#         ("R2", "L22"),
#         ("1L", "L1"),
#         ("2L1", "22R"),
#         ("2L2", "L22"),
#         ("/L2", "/1C"),
#         ("C2", "1C"),
#         ("C/", "/"),
#     ]
# )

# # app.make_step()
# app.run()
