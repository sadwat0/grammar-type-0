"""Implements Rule class"""


class Rule:
    def __init__(self, original: list[str], replacement: list[str]):
        self.original = original
        self.replacement = replacement

    def find_position(self, state: list[str]) -> int | None:
        """Returns index of {self.original} occurence in state.

        Args:
            state (str): string in which to find

        Returns:
            int: None if {self.original} is not occured in state,
                 index of occurence begin if {self.original} occurs exactly once
                 -1 else
        """

        # occurences = [m.start(0) for m in re.finditer(self.original, state)]
        occurences = []
        for begin_idx in range(len(state) - len(self.original) + 1):
            if state[begin_idx : begin_idx + len(self.original)] == self.original:
                occurences.append(begin_idx)

        if len(occurences) == 0:
            return None
        if len(occurences) > 1:
            return -1

        return occurences[0]

    def apply(self, state: list[str], position: int | None = None) -> str | None:
        """Applies rule to given state if possible.

        Args:
            state (str): state to check
            position (int | None, optional): _description_. Defaults to None.

        Returns:
            str | None: new state or None if can't be applied
        """

        # find position if not set
        if position is None:
            position = self.find_position(state)

        # check if can apply
        if position is None or position == -1:
            return None

        new_state = (
            state[:position] + self.replacement + state[position + len(self.original) :]
        )
        return new_state

    def __eq__(self, other):
        if isinstance(other, Rule):
            return (
                self.original == other.original
                and self.replacement == other.replacement
            )
        return False
