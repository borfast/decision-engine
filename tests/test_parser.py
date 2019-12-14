import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from decision_engine import parser


schema_file = 'schema.json'
schema_path = (Path(__file__).parents[1] / 'decision_engine' / schema_file).absolute()
test_definition = 'test_definition.json'
definition_path = (Path(__file__).parents[0] / test_definition).absolute()


def load_json_file(file: str):
    with (open(file)) as fp:
        contents = json.load(fp)
    return contents


def test_sources_parsed_correctly():
    definition = load_json_file(definition_path)
    sources = parser.parse_sources(definition['sources'])
    assert len(sources) == 2


# def test_final_engine_works_correctly():
#     pass

# These are probably not needed, since what we're really doing here is
# testing jsonschema's package validation capabilities, which should be
# done in its own package, not here.
def test_validation_passes_with_valid_definition():
    schema = load_json_file(schema_path)
    definition = load_json_file(definition_path)
    parser.validate(definition, schema)


def test_validation_fails_with_invalid_definition():
    schema = load_json_file(schema_path)
    definition = load_json_file(definition_path)

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
