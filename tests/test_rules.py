# coding=utf-8
import pytest

from decision_engine.comparisons import Equal, GreaterThanOrEqual
from decision_engine.rules import SimpleRule, BooleanOrRule, BooleanAndRule
from decision_engine.sources import DictSource, FixedValueSource


@pytest.mark.parametrize('smoker, expected', [
    (True, False),
    (False, True)
])
def test_simple_rule(smoker, expected):
    smoker_source = DictSource('smoker')
    non_smoker_requirement = FixedValueSource(False)
    rule = SimpleRule(smoker_source, non_smoker_requirement, Equal())

    data = {
        'smoker': smoker
    }

    assert rule.check(data) is expected


@pytest.mark.parametrize('colour, expected', [
    ('red', True),
    ('blue', True),
    ('brown', False)
])
def test_or_boolean_rule(colour, expected):
    colour_source = DictSource('colour')
    colour_requirement1 = FixedValueSource('blue')
    colour_requirement2 = FixedValueSource('red')
    rule1 = SimpleRule(colour_source, colour_requirement1, Equal())
    rule2 = SimpleRule(colour_source, colour_requirement2, Equal())

    rule = BooleanOrRule(rule1, rule2)

    data = {
        'colour': colour
    }

    assert rule.check(data) is expected


@pytest.mark.parametrize('age, smoker, expected', [
    (18, False, True),
    (18, True, False),
    (15, False, False),
])
def test_and_boolean_rule(age, smoker, expected):
    age_source = DictSource('age')
    age_requirement = FixedValueSource(18)
    rule1 = SimpleRule(age_source, age_requirement, GreaterThanOrEqual())

    smoker_source = DictSource('smoker')
    smoker_requirement = FixedValueSource(False)
    rule2 = SimpleRule(smoker_source, smoker_requirement, Equal())

    rule = BooleanAndRule(rule1, rule2)

    data = {
        'age': age,
        'smoker': smoker
    }

    assert rule.check(data) is expected
