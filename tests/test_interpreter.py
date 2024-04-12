# TODO: add stronger tests

from src.rule import Rule
from src.constants import Dividers
from src.interpreter import BaseInterpreter, Interpreter


def test_base_interpreter_init():
    interpreter = BaseInterpreter(
        rules=[Rule("A", "B")], state=["A"], divider=Dividers.NONE
    )
    assert interpreter.rules == [Rule("A", "B")]
    assert interpreter.state == ["A"]
    assert interpreter.divider == Dividers.NONE
    assert interpreter.steps_count == 0
    assert not interpreter.is_ended


def test_base_interpreter_add_rule():
    interpreter = BaseInterpreter()
    interpreter.add_rule(Rule("A", "B"))
    assert interpreter.rules == [Rule("A", "B")]
    assert not interpreter.is_ended


def test_base_interpreter_set_rules():
    interpreter = BaseInterpreter()
    interpreter.set_rules([Rule("A", "B"), Rule("B", "C")])
    assert interpreter.rules == [Rule("A", "B"), Rule("B", "C")]
    assert not interpreter.is_ended

    interpreter.set_rules([("A", "B"), ("B", "C")])
    assert interpreter.rules == [Rule("A", "B"), Rule("B", "C")]
    assert not interpreter.is_ended


def test_base_interpreter_set_state():
    interpreter = BaseInterpreter(divider=Dividers.NONE)
    interpreter.set_state(["A", "B"])
    assert interpreter.state == ["A", "B"]
    assert not interpreter.is_ended

    interpreter.set_state("ABC")
    assert interpreter.state == ["A", "B", "C"]
    assert not interpreter.is_ended


def test_base_interpreter_end():
    interpreter = BaseInterpreter()
    interpreter.end()
    assert interpreter.is_ended is True


def test_base_interpreter_make_step():
    interpreter = BaseInterpreter(
        rules=[Rule(["A"], ["B"])], state=["A", "C"], divider=Dividers.NONE
    )
    new_state = interpreter.make_step()
    assert new_state == ["B", "C"]
    assert interpreter.state == ["B", "C"]
    assert interpreter.steps_count == 1

    interpreter.end()
    new_state = interpreter.make_step()
    assert new_state is None


def test_base_interpreter_make_steps():
    interpreter = BaseInterpreter(
        rules=[Rule(["B"], ["A'"]), Rule(["A", "A'"], ["B"])],
        state=["A", "B", "C"],
        divider=Dividers.SPACES,
    )
    new_state = interpreter.make_steps(2)
    assert new_state == ["B", "C"]
    assert interpreter.state == ["B", "C"]
    assert interpreter.steps_count == 2

    interpreter.end()
    new_state = interpreter.make_steps()
    assert new_state is None


def test_interpreter_make_step():
    interpreter = Interpreter(
        rules=[Rule(["A"], ["B"])], state=["A"], divider=Dividers.NONE, verbose=False
    )
    new_state = interpreter.make_step()
    assert new_state == ["B"]
    assert interpreter.state == ["B"]
    assert interpreter.steps_count == 1

    interpreter.end()
    new_state = interpreter.make_step()
    assert new_state is None


def test_interpreter_run():
    interpreter = Interpreter(
        rules=[Rule(["A"], ["B"]), Rule(["B"], ["C"])],
        state=["A"],
        divider=Dividers.NONE,
        verbose=False,
    )
    interpreter.run()
    assert interpreter.state == ["C"]
    assert interpreter.steps_count == 2
