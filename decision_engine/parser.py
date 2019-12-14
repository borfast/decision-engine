import importlib
import json
from pathlib import Path
from typing import List

import jsonschema


# TODO: Make sure the classes specified in the schema exist in Python.
#  Perhaps that part of the schema should be generated automatically.

# TODO: iterate over rules and create each rule,
#  iterate over engines and create each engine,
#  make parsing recursive for composition.
from decision_engine.sources import Source


def load_json_file(file: str):
    with (open(file)) as fp:
        contents = json.load(fp)
    return contents


def validate(definition: dict, schema: dict):
    jsonschema.validate(instance=definition, schema=schema)


def parse_sources(sources: List[dict]) -> List[Source]:
    final_sources = []
    for source in sources:
        class_name = source['class']
        module = importlib.import_module('decision_engine.sources')
        class_ = getattr(module, class_name)
        instance = class_(*source['params'])
        final_sources.append(instance)

    return final_sources


def parse_json(definition: dict) -> list:
    schema_file = 'schema.json'
    schema_path = (Path(__file__).parents[0] / schema_file).absolute()
    schema = load_json_file(schema_path)
    validate(definition, schema)

    parse_sources(definition['sources'])

    return []


def parse_json_file(file: str) -> list:
    definition = load_json_file(file)
    return parse_json(definition)
