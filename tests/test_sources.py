# coding=utf-8
from decision_engine.sources import DictSource, FixedValueSource, \
    PercentageSource


def test_dict_source():
    test_key = 'test_key'
    test_value = 5000
    data = {test_key: test_value}

    src = DictSource(test_key)

    assert src.get_value(data) == test_value


def test_fixed_value_source():
    test_value = 5000
    src = FixedValueSource(test_value)

    assert src.get_value() == test_value


def test_percentage_value_source():
    test_value = 75000
    data = {
        'test_value': 100000
    }
    src = PercentageSource('0.75', DictSource('test_value'))

    assert src.get_value(data) == test_value
