import importlib
import json
from pathlib import Path
from typing import List

import jsonschema
from jsonschema import ValidationError

from decision_engine.engine import Engine
from decision_engine.rules import Rule
from decision_engine.sources import Source

param_types_table = {
    'boolean': bool,
    'float': float,
    'integer': int,
    'string': str,
    'source': str
}


def load_json_file(file: str) -> dict:
    with (open(file)) as fp:
        contents = json.load(fp)
    return contents


def validate(definition: dict, schema: dict):
    jsonschema.validate(instance=definition, schema=schema)


def _check_param_type(param: dict):
    param_type = param_types_table[param['type']]
    if not isinstance(param['value'], param_type):
        msg = f"Parameter declared with type {param['type']}" \
              f"(Python type {param_type}) " \
              f"but value is of type {type(param['value']).__name__}."
        raise ValidationError(msg)


def _check_source_param_exists(param: dict, sources: dict):
    if param['value'] not in sources.keys():
        msg = f'Parameter declared as source but specified source ' \
              f'{param["value"]} has not been parsed yet. ' \
              f'Please rectify your definition file.'
        raise ValidationError(msg)


def _parse_params(params: dict, parsed_sources: List[Source]) -> list:
    result = []
    sources_dict = {source.name: source for source in parsed_sources}
    for param in params:
        _check_param_type(param)

        if param['type'] == 'source':
            _check_source_param_exists(param, sources_dict)
            param['value'] = sources_dict[param['value']]

        result.append(param['value'])

    return result


def parse_sources(sources: List[dict]) -> List[Source]:
    final_sources: List[Source] = []
    module = importlib.import_module('decision_engine.sources')
    for source in sources:
        class_name = source['class']
        class_ = getattr(module, class_name)
        params = _parse_params(source['params'], final_sources)
        instance = class_(*params, source['name'])
        final_sources.append(instance)

    return final_sources


def parse_rules(rules: List[dict], sources: List[Source]) -> List[Rule]:
    final_rules = []
    rules_module = importlib.import_module('decision_engine.rules')
    comparisons_module = importlib.import_module('decision_engine.comparisons')
    for rule in rules:
        rules_class = getattr(rules_module, rule['class'])
        comparison_class = getattr(comparisons_module, rule['comparison'])

        # Create a new list containing only the sources named in the rule.
        rule_sources = [
            source for source in sources
            if source.name in rule['sources']
        ]

        instance = rules_class(*rule_sources, comparison_class(), rule['name'])
        final_rules.append(instance)

    return final_rules


def parse_engines(engines: List[dict], rules: List[Rule]) -> List[Engine]:
    final_engines = []
    for engine in engines:
        # Create a new list containing only the rules named in the engine.
        engine_rules = [rule for rule in rules if rule.name in engine['rules']]

        instance = Engine(engine_rules, engine['name'])
        final_engines.append(instance)

    return final_engines


def parse_json(definition: dict) -> dict:
    schema_file = 'schema.json'
    schema_path = (Path(__file__).parents[0] / schema_file).absolute()
    schema = load_json_file(str(schema_path))
    validate(definition, schema)

    sources = parse_sources(definition['sources'])
    rules = parse_rules(definition['rules'], sources)
    engines = parse_engines(definition['engines'], rules)

    return {'sources': sources, 'rules': rules, 'engines': engines}


def parse_json_file(file: str) -> dict:
    definition = load_json_file(file)
    return parse_json(definition)
