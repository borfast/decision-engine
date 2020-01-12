# coding=utf-8
from decision_engine.sources import DictSource, FixedValueSource, \
    PercentageSource, RandomIntSource


def test_dict_source():
    test_key = 'test_key'
    test_value = 5000
    data = {test_key: test_value}

    # Test source with normal data
    src = DictSource('dict source', test_key)
    assert src.get_value(data) == test_value

    # Test source with data set to None
    assert src.get_value() is None


def test_fixed_value_source():
    test_value = 5000
    src = FixedValueSource('fixed value source', test_value)

    assert src.get_value() == test_value


def test_percentage_value_source():
    test_value = 75000
    data = {
        'test_value': 100000
    }
    src = PercentageSource('percentage source', 0.75,
                           DictSource('dict source', 'test_value'))

    assert src.get_value(data) == test_value


def test_random_int_source():
    max_test_value = 120
    min_test_value = 12

    # Test random source without explicit seed
    src = RandomIntSource('random int 1', min_test_value, max_test_value)
    assert min_test_value <= src.get_value() <= max_test_value

    # Test random source with explicit seed
    src = RandomIntSource('random int 2', min_test_value, max_test_value,
                          12345)
    assert min_test_value <= src.get_value() <= max_test_value
