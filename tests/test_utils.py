import pytest
from src.constants import Dividers
from src.utils import state_to_string


def test_state_to_string_none_divider():
    state = ["A", "B", "C"]
    divider = Dividers.NONE

    assert state_to_string(state, divider) == "ABC"


def test_state_to_string_spaces_divider():
    state = ["A", "B", "C"]
    divider = Dividers.SPACES

    assert state_to_string(state, divider) == "A, B, C"


def test_state_to_string_not_set_divider():
    state = ["A", "B", "C"]
    divider = Dividers.NOT_SET

    with pytest.raises(ValueError):
        state_to_string(state, divider)
