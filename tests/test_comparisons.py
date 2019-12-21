from decision_engine.comparisons import GreaterThan, GreaterThanOrEqual, \
    LessThan, LessThanOrEqual, Equal, NotEqual, NoOp


def test_no_op():
    comp = NoOp()
    assert comp.check(False, False)


def test_equal():
    comp = Equal()
    assert comp.check(10, 10)
    assert not comp.check(10, 20)


def test_not_equal():
    comp = NotEqual()
    assert comp.check(10, 20)
    assert not comp.check(10, 10)


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
