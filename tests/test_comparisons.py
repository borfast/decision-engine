from decision_engine.comparisons import GreaterThan, GreaterThanOrEqual, \
    LessThan, LessThanOrEqual, Equal


def test_equal():
    comp = Equal()
    assert comp.check(10, 10)
    assert not comp.check(10, 11)


def test_greater_than():
    comp = GreaterThan()
    assert comp.check(10, 5)
    assert not comp.check(10, 50)


def test_greater_than_or_equal():
    comp = GreaterThanOrEqual()
    assert comp.check(10, 5)
    assert comp.check(10, 10)
    assert not comp.check(10, 50)


def test_less_than():
    comp = LessThan()
    assert comp.check(5, 10)
    assert not comp.check(50, 10)


def test_less_than_or_equal():
    comp = LessThanOrEqual()
    assert comp.check(5, 10)
    assert comp.check(5, 5)
    assert not comp.check(50, 5)
