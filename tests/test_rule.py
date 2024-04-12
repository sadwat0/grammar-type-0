from src.rule import Rule


def test_find_position_not_found():
    rule = Rule(["A", "B", "C"], ["X", "Y", "Z"])
    state = ["D", "E", "F"]
    assert rule.find_position(state) is None


def test_find_position_found_once():
    rule = Rule(["A", "B", "C"], ["X", "Y", "Z"])
    state = ["D", "A", "B", "C", "E"]
    assert rule.find_position(state) == 1


def test_find_position_found_multiple():
    rule = Rule(["A", "B", "C"], ["X", "Y", "Z"])
    state = ["A", "B", "C", "D", "A", "B", "C"]
    assert rule.find_position(state) == -1


def test_apply_not_applicable():
    rule = Rule(["A", "B", "C"], ["X", "Y", "Z"])
    state = ["D", "E", "F"]
    assert rule.apply(state) is None


def test_apply_applicable():
    rule = Rule(["A", "B", "C"], ["X", "Y", "Z"])
    state = ["D", "A", "B", "C", "E"]
    assert rule.apply(state) == ["D", "X", "Y", "Z", "E"]


def test_apply_applicable_double_chars():
    rule = Rule(["A_", "_", "__"], ["XX", "YY", "ZZ"])
    state = ["DD", "A_", "_", "__", "EE"]
    assert rule.apply(state) == ["DD", "XX", "YY", "ZZ", "EE"]


def test_apply_position_specified():
    rule = Rule(["A", "B", "C"], ["X", "Y", "Z"])
    state = ["A", "B", "C", "D", "A", "B", "C"]
    assert rule.apply(state, position=0) == ["X", "Y", "Z", "D", "A", "B", "C"]
