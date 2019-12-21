# coding=utf-8
from decision_engine.sources import DictSource, FixedValueSource, \
    PercentageSource, RandomIntSource


def test_dict_source():
    test_key = 'test_key'
    test_value = 5000
    data = {test_key: test_value}

    # Test source with normal data
    src = DictSource(test_key)
    assert src.get_value(data) == test_value

    # Test source with data set to None
    assert src.get_value() is None

    assert src.__repr__() == f"Name: '{src.name}' | key: '{src.key}'"


def test_fixed_value_source():
    test_value = 5000
    src = FixedValueSource(test_value)

    assert src.get_value() == test_value
    assert src.__repr__() == f"Name: '{src.name}' | value: {src.value}"


def test_percentage_value_source():
    test_value = 75000
    data = {
        'test_value': 100000
    }
    src = PercentageSource(0.75, DictSource('test_value'))

    assert src.get_value(data) == test_value
    assert src.__repr__() == f"Name: '{src.name}' | " \
                             f"percentage: {src.percentage} | " \
                             f"source: '{src.source.name}'"


def test_random_int_source():
    max_test_value = 120
    min_test_value = 12

    # Test random source without explicit seed
    src = RandomIntSource(min_test_value, max_test_value)
    assert min_test_value <= src.get_value() <= max_test_value

    # Test random source with explicit seed
    src = RandomIntSource(min_test_value, max_test_value, 12345)
    assert min_test_value <= src.get_value() <= max_test_value

    # Check the name
    assert src.__repr__() == f"Name: '{src.name}' | " \
                             f"min_value: {src.min_value} | " \
                             f"max_value: {src.max_value} | " \
                             f"seed: {src.seed}"
