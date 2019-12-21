import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from decision_engine import parser


defs_dir = Path(__file__).parents[0] / 'test_definitions'
schema_dir = defs_dir.parents[1] / 'decision_engine'

schema_file = 'schema.json'
schema_path = schema_dir / schema_file

definition_path = defs_dir / 'test_definition.json'
nested_sources_def_path = defs_dir / 'test_nested_sources.json'
full_def_path = defs_dir / 'full_definition.json'


def _load_json_file(file: str) -> dict:
    with (open(file)) as fp:
        contents = json.load(fp)
    return contents


@pytest.mark.parametrize('definition_file', [
    definition_path,
    nested_sources_def_path,
    full_def_path
])
def test_sources_parsed_correctly(definition_file):
    definition = _load_json_file(definition_file)
    sources = parser.parse_sources(definition['sources'])
    assert len(sources) == len(definition['sources'])
    for i in range(len(definition['sources'])):
        assert sources[i].name == definition['sources'][i]['name']
        assert type(sources[i]).__name__ == definition['sources'][i]['class']


def test_rules_parsed_correctly():
    definition = _load_json_file(definition_path)
    sources = parser.parse_sources(definition['sources'])
    rules = parser.parse_rules(definition['rules'], sources)
    assert len(rules) == len(definition['rules'])
    for i in range(len(definition['rules'])):
        assert rules[i].name == definition['rules'][i]['name']
        assert type(rules[i]).__name__ == definition['rules'][i]['class']


def test_engines_parsed_correctly():
    definition = _load_json_file(definition_path)
    sources = parser.parse_sources(definition['sources'])
    rules = parser.parse_rules(definition['rules'], sources)
    engines = parser.parse_engines(definition['engines'], rules)
    assert len(engines) == len(definition['engines'])
    for i in range(len(definition['engines'])):
        assert engines[i].name == definition['engines'][i]['name']
        assert len(engines[i].rules) == len(rules)


def test_valid_test_definition():
    """
    Make sure our test definition is valid,
    otherwise there's no point in using it for testing.
    """
    schema = _load_json_file(schema_path)
    definition = _load_json_file(definition_path)
    parser.validate(definition, schema)


@pytest.mark.parametrize('file_name', [
    'wrong_param_type.json',
    'inexistent_source.json',
    'inexistent_rule.json'
])
def test_validation_errors(file_name):
    with pytest.raises(ValidationError):
        path = defs_dir / file_name
        parser.parse_json_file(path)


@pytest.mark.parametrize("air_miles, land_miles, age, vip, expected", [
    (500, 100, 37, 'yes', True),
    (150, 100, 37, 'yes', False),
    (500, 501, 37, 'yes', False),
    (500, 100, 16, 'yes', False),
    (500, 100, 70, 'yes', False),
    (500, 100, 37, 'no', False),
    (10, 50, 15, 'no', False)
])
def test_fully_parsed_engine(air_miles, land_miles, age, vip, expected):
    engines = parser.parse_json_file(full_def_path)

    engine = engines['engines'][0]

    data = {
        'air_miles': air_miles,
        'land_miles': land_miles,
        'age': age,
        'vip': vip
    }

    assert engine.decide(data) == expected


# These are probably not needed, since what we're really doing here is
# testing that jsonschema validates correctly, which should be done in
# its own package, not here.
def test_validation_fails_with_invalid_definition():
    schema = _load_json_file(schema_path)
    definition = _load_json_file(definition_path)

    definition_without_sources = definition.copy()
    del definition_without_sources['sources']
    with pytest.raises(ValidationError):
        parser.validate(definition_without_sources, schema)

    definition_without_rules = definition.copy()
    del definition_without_rules['rules']
    with pytest.raises(ValidationError):
        parser.validate(definition_without_rules, schema)

    definition_without_engines = definition.copy()
    del definition_without_engines['engines']
    with pytest.raises(ValidationError):
        parser.validate(definition_without_engines, schema)
