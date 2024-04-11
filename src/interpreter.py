"""Implements interpreter classes"""

from typing import TypeAlias
from loguru import logger
from src.rule import Rule
from src import constants
from src.constants import Dividers
from src.utils import state_to_string

Sequence: TypeAlias = list[str]


class BaseInterpreter:
    def __init__(
        self,
        rules: list[Rule] = None,
        state: Sequence = None,
        divider: Dividers = None,
    ):
        self.rules: list[Rule] = rules
        self.divider: Dividers = divider
        self.state: Sequence = state

        self.steps_count: int = 0
        self.is_ended: bool = False

    def add_rule(self, rule: Rule) -> None:
        """Adds {rule} to list of rules.

        WARNING: if you want to add a lot rules you should use Interpreter.set_rules().

        Args:
            rule (Rule): rule to add.
        """

        if rule not in self.rules:
            self.rules.append(rule)
            self.is_ended = False

    def set_rules(self, rules: list[Rule] | list[tuple[Sequence, Sequence]]) -> None:
        """Updates rules. Erases old rules.

        Args:
            rules (list[Rule]): list of new rules
        """

        if len(rules) and not isinstance(rules[0], Rule):
            # rules is list[tuple[str, str]]
            self.rules = [
                Rule(original, replacement) for original, replacement in rules
            ]
        else:
            self.rules = rules

        self.is_ended = False

    def set_state(self, state: list[str] | str) -> None:
        """Updates state. Erases old state.

        Args:
            state (list[str] | str): new state, string can be passed if divider is Dividers.NONE
        """

        if isinstance(state, str) and self.divider is not Dividers.NONE:
            logger.warning(
                "divider is not set before settings state with str"
                ", it would become Dividers.NONE"
            )

            self.divider = Dividers.NONE

        self.state = list(state)
        self.is_ended = False

    def end(self) -> None:
        self.is_ended = True

    def make_step(self) -> Sequence | None:
        """Makes one step.

        Returns:
            Sequence | None: new state if successfull, else None
        """

        if self.is_ended or self.steps_count >= constants.STEPS_LIMIT:
            return None

        new_state = None
        applied = False

        for rule in self.rules:
            position = rule.find_position(self.state)
            if position == -1 or (position is not None and applied):
                return None

            if position is not None:
                applied = True
                new_state = rule.apply(self.state, position=position)

        if applied is False:
            self.is_ended = True

        if new_state is not None:
            self.state = new_state
            self.steps_count += 1

        return new_state

    def make_steps(self, count: int = 1) -> str | None:
        """Makes {count} steps.

        Args:
            count (int, optional): how many steps to do

        Returns:
            str | None: new state if successfull, else None
        """

        new_state = self.state

        for _ in range(count):
            new_state = self.make_step()
            if new_state is None:
                return None

        return new_state


class Interpreter(BaseInterpreter):
    def __init__(
        self, rules: list[Rule] = None, state: Sequence = None, verbose: bool = False
    ):
        super().__init__(rules, state)
        self.verbose = verbose

    def make_step(self) -> str | None:
        old_state = self.state
        result = super().make_step()

        if result is None:
            if self.is_ended:
                if self.verbose:
                    logger.warning("called make_step() on ended state")
                return

            logger.error("wrong call of make_step()")
        else:
            logger.info(
                f"[{self.steps_count}] {state_to_string(old_state, self.divider)} -> "
                f"{state_to_string(result, self.divider)}"
            )

        return self.state

    def run(self):
        """Makes steps until can and limit not reached"""

        logger.info(f"run started with {state_to_string(self.state, self.divider)}")
        begin_steps_count = self.steps_count

        while not self.is_ended:
            result = self.make_step()
            if result is None:
                break

        logger.success(
            f"run ended in {self.steps_count - begin_steps_count} steps "
            f"with {state_to_string(self.state, self.divider)}"
        )
