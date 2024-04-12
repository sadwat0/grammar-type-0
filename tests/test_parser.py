import pytest
from src.constants import Dividers
from src.rule import Rule
from src.parser import Parser


def test_parse_divider_valid():
    parser = Parser()
    strings = ["divider = spaces"]
    assert parser.parse_divider(strings) is True
    assert parser.divider == Dividers.SPACES


def test_parse_divider_unknown_type():
    parser = Parser()
    strings = ["divider = unknown"]
    assert parser.parse_divider(strings) is False


def test_parse_divider_different_dividers():
    parser = Parser()
    strings = ["divider = spaces", "divider = none"]
    assert parser.parse_divider(strings) is False

    parser2 = Parser()
    strings2 = ["divider = spaces = none = spaces"]
    assert parser2.parse_divider(strings2) is False


def test_parse_divider_default():
    parser = Parser()
    strings = ["A -> B"]
    assert parser.parse_divider(strings) is True
    assert parser.divider == Dividers.NONE


def test_parse_rules_valid():
    parser = Parser()
    parser.divider = Dividers.SPACES
    strings = ["A B C -> D E F", "G H I -> J K L"]
    assert parser.parse_rules(strings) is True
    assert len(parser.rules) == 2
    assert parser.rules[0] == Rule(["A", "B", "C"], ["D", "E", "F"])
    assert parser.rules[1] == Rule(["G", "H", "I"], ["J", "K", "L"])


def test_parse_rules_invalid_format():
    parser = Parser()
    parser.divider = Dividers.SPACES
    strings = ["A B C D E F", "G H I -> J K L"]
    assert parser.parse_rules(strings) is False


def test_parse_rules_divider_not_set():
    parser = Parser()
    strings = ["A B C -> D E F", "G H I -> J K L"]
    with pytest.raises(RuntimeError):
        parser.parse_rules(strings)


def test_update_from_strings_valid():
    parser = Parser()
    strings = ["divider = spaces", "A B C -> D E F", "G H I -> J K L"]
    assert parser.update_from_strings(strings) is True
    assert parser.divider == Dividers.SPACES
    assert len(parser.rules) == 2
    assert parser.rules[0] == Rule(["A", "B", "C"], ["D", "E", "F"])
    assert parser.rules[1] == Rule(["G", "H", "I"], ["J", "K", "L"])


def test_update_from_strings_invalid():
    parser = Parser()
    strings = ["divider = some_unknown_divider", "A B C -> D E F", "G H I -> J K L"]
    assert parser.update_from_strings(strings) is False


def test_get_rules():
    parser = Parser()
    parser.rules = [
        Rule(["A", "B", "C"], ["D", "E", "F"]),
        Rule(["G", "H", "I"], ["J", "K", "L"]),
    ]
    rules = parser.get_rules()
    assert len(rules) == 2
    assert rules[0] == Rule(["A", "B", "C"], ["D", "E", "F"])
    assert rules[1] == Rule(["G", "H", "I"], ["J", "K", "L"])
