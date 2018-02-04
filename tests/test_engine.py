# coding=utf-8
import pytest

from decision_engine.comparisons import GreaterThanOrEqual, Equal, \
    LessThanOrEqual
from decision_engine.engine import Engine
from decision_engine.rules import Rule
from decision_engine.sources import DictSource, FixedValueSource, \
    PercentageSource


@pytest.mark.parametrize("salary, expected", [
    (100000, True),
    (10000, False)
])
def test_single_rule_engine(salary, expected):
    salary_percentage = PercentageSource(0.75, DictSource('salary'))
    minimum_salary = FixedValueSource(50000)
    rule = Rule(salary_percentage, minimum_salary, GreaterThanOrEqual())
    engine = Engine([rule])

    data = {
        'salary': salary
    }

    assert engine.decide(data) == expected


@pytest.mark.parametrize("air_miles, land_miles, age, vip, expected", [
    (5000, 1000, 37, 'yes', True),
    (1500, 1000, 37, 'yes', False),
    (5000, 5001, 37, 'yes', False),
    (5000, 1000, 16, 'yes', False),
    (5000, 1000, 70, 'yes', False),
    (5000, 1000, 37, 'no', False),
    (100, 50, 15, 'no', False)
])
def test_multiple_rules_engine(air_miles, land_miles, age, vip, expected):
    air_miles_source = DictSource('air_miles')
    minimum_miles_source = FixedValueSource(3500)
    rule1 = Rule(air_miles_source, minimum_miles_source, GreaterThanOrEqual())

    land_miles_source = DictSource('land_miles')
    rule2 = Rule(land_miles_source, air_miles_source, LessThanOrEqual())

    age_source = DictSource('age')
    minimum_age_source = FixedValueSource(21)
    rule3 = Rule(age_source, minimum_age_source, GreaterThanOrEqual())

    maximum_age_source = FixedValueSource(65)
    rule4 = Rule(age_source, maximum_age_source, LessThanOrEqual())

    vip_status_source = DictSource('vip')
    positive_vip_status = FixedValueSource('yes')
    rule5 = Rule(vip_status_source, positive_vip_status, Equal())

    engine = Engine([rule1, rule2, rule3, rule4, rule5])

    data = {
        'air_miles': air_miles,
        'land_miles': land_miles,
        'age': age,
        'vip': vip
    }

    assert engine.decide(data) == expected
