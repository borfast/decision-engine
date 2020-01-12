# coding=utf-8
import pytest

from decision_engine.comparisons import GreaterThanOrEqual, Equal, \
    LessThanOrEqual
from decision_engine.engine import Engine
from decision_engine.rules import SimpleComparisonRule, BooleanAndRule
from decision_engine.sources import DictSource, FixedValueSource, \
    PercentageSource


def test_single_stupid_rule_engine():
    hundred = FixedValueSource('hundred', 100)
    five_thousand = FixedValueSource('five_thousand', 5000)
    rule = SimpleComparisonRule(five_thousand, hundred, GreaterThanOrEqual())
    engine = Engine([rule])

    data = {}

    assert engine.decide(data) is True
    assert engine.__repr__() == f"Name: '{engine.name}' | " \
                                f"rules: {[r.name for r in engine.rules]}"


@pytest.mark.parametrize("salary, expected", [
    (100000, True),
    (10000, False)
])
def test_single_rule_engine(salary, expected):
    salary_percentage = PercentageSource('salary percentage', 0.75,
                                         DictSource('salary dict', 'salary'))
    minimum_salary = FixedValueSource('minimum salary', 50000)
    rule = SimpleComparisonRule(salary_percentage, minimum_salary,
                                GreaterThanOrEqual())
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
    air_miles_source = DictSource('air miles', 'air_miles')
    minimum_miles_source = FixedValueSource('minimum air miles', 3500)
    minimum_air_miles_rule = SimpleComparisonRule(air_miles_source,
                                                  minimum_miles_source,
                                                  GreaterThanOrEqual())

    land_miles_source = DictSource('land miles', 'land_miles')
    less_land_than_air_miles_rule = SimpleComparisonRule(land_miles_source,
                                                         air_miles_source,
                                                         LessThanOrEqual())

    air_miles_percentage = PercentageSource('air miles percentage', 0.05,
                                            air_miles_source)
    air_miles_percentage_rule = SimpleComparisonRule(land_miles_source,
                                                     air_miles_percentage,
                                                     GreaterThanOrEqual())

    air_and_land_miles_rule = BooleanAndRule([minimum_air_miles_rule,
                                              less_land_than_air_miles_rule,
                                              air_miles_percentage_rule])

    age_source = DictSource('age', 'age')
    minimum_age_source = FixedValueSource('minimum age', 21)
    minimum_age_rule = SimpleComparisonRule(age_source, minimum_age_source,
                                            GreaterThanOrEqual())

    maximum_age_source = FixedValueSource('maximum age', 65)
    maximum_age_rule = SimpleComparisonRule(age_source, maximum_age_source,
                                            LessThanOrEqual())

    vip_status_source = DictSource('vip', 'vip')
    positive_vip_status = FixedValueSource('is vip', 'yes')
    vip_status_rule = SimpleComparisonRule(vip_status_source,
                                           positive_vip_status,
                                           Equal())

    engine = Engine([
        air_and_land_miles_rule,
        minimum_age_rule,
        maximum_age_rule,
        vip_status_rule
    ])

    data = {
        'air_miles': air_miles,
        'land_miles': land_miles,
        'age': age,
        'vip': vip
    }

    assert engine.decide(data) == expected
