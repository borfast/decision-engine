# coding=utf-8
import pytest

from decision_engine.comparisons import Equal, GreaterThanOrEqual
from decision_engine.rules import SimpleComparisonRule, BooleanOrRule, BooleanAndRule
from decision_engine.sources import DictSource, FixedValueSource


@pytest.mark.parametrize('smoker, expected', [
    (True, False),
    (False, True)
])
def test_simple_comparison_rule(smoker, expected):
    smoker_source = DictSource('smoker')
    non_smoker_requirement = FixedValueSource(False)
    rule = SimpleComparisonRule(smoker_source, non_smoker_requirement, Equal())

    data = {
        'smoker': smoker
    }

    assert rule.check(data) is expected


@pytest.mark.parametrize('colour, expected', [
    ('red', True),
    ('blue', True),
    ('yellow', True),
    ('brown', False),
    ('black', False)
])
def test_boolean_or_rule(colour, expected):
    """The colour source must match at least one of the two required colours."""
    colour_source = DictSource('colour')
    colour_requirement1 = FixedValueSource('blue')
    colour_requirement2 = FixedValueSource('red')
    colour_requirement3 = FixedValueSource('yellow')
    rule1 = SimpleComparisonRule(colour_source, colour_requirement1, Equal())
    rule2 = SimpleComparisonRule(colour_source, colour_requirement2, Equal())
    rule3 = SimpleComparisonRule(colour_source, colour_requirement3, Equal())

    rule = BooleanOrRule([rule1, rule2, rule3])

    data = {
        'colour': colour
    }

    assert rule.check(data) is expected


@pytest.mark.parametrize('age, smoker, voted_for_trump, expected', [
    (18, False, False, True),
    (18, False, True, False),
    (18, True, False, False),
    (18, True, True, False),
    (15, False, False, False),
    (15, False, True, False),
    (15, True, False, False),
    (15, True, True, False)
])
def test_boolean_and_rule(age, smoker, voted_for_trump, expected):
    """Only people 18+ years old, non-smokers, and who did not vote for Trump are allowed."""
    age_source = DictSource('age')
    age_requirement = FixedValueSource(18)
    rule1 = SimpleComparisonRule(age_source, age_requirement, GreaterThanOrEqual())

    smoker_source = DictSource('smoker')
    smoker_requirement = FixedValueSource(False)
    rule2 = SimpleComparisonRule(smoker_source, smoker_requirement, Equal())

    voter_source = DictSource('voted_for_trump')
    voter_requirement = FixedValueSource(False)
    rule3 = SimpleComparisonRule(voter_source, voter_requirement, Equal())

    rule = BooleanAndRule([rule1, rule2, rule3])

    data = {
        'age': age,
        'smoker': smoker,
        'voted_for_trump': voted_for_trump
    }

    assert rule.check(data) is expected
