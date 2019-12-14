import importlib
import json
from pathlib import Path
from typing import List

import jsonschema

from decision_engine.engine import Engine
from decision_engine.rules import Rule
from decision_engine.sources import Source


def load_json_file(file: str):
    with (open(file)) as fp:
        contents = json.load(fp)
    return contents


def validate(definition: dict, schema: dict):
    jsonschema.validate(instance=definition, schema=schema)


def parse_sources(sources: List[dict]) -> List[Source]:
    """
    TODO: Make sure the classes specified in the schema exist in Python.
          Perhaps that part of the schema should be generated automatically.
    TODO: make parsing recursive for composition.
    """
    final_sources = []
    module = importlib.import_module('decision_engine.sources')
    for source in sources:
        class_name = source['class']
        class_ = getattr(module, class_name)
        instance = class_(*source['params'], source['name'])
        final_sources.append(instance)

    return final_sources


def parse_rules(rules: List[dict], sources: List[Source]) -> List[Rule]:
    """
    TODO: Make sure the classes specified in the schema exist in Python.
          Perhaps that part of the schema should be generated automatically.
    TODO: make parsing recursive for composition.
    """
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

        engine = Engine(engine_rules, engine['name'])
        final_engines.append(engine)

    return final_engines


def parse_json(definition: dict) -> dict:
    schema_file = 'schema.json'
    schema_path = (Path(__file__).parents[0] / schema_file).absolute()
    schema = load_json_file(schema_path)
    validate(definition, schema)

    sources = parse_sources(definition['sources'])
    rules = parse_rules(definition['rules'], sources)
    engines = parse_engines(definition['engines'], rules)

    return {'sources': sources, 'rules': rules, 'engines': engines}


def parse_json_file(file: str) -> dict:
    definition = load_json_file(file)
    return parse_json(definition)
