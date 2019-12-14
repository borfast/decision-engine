import json

import jsonschema


# TODO: make parser use validation automatically,
#  make validator throw exception,
#  iterate over sources and create each Source,
#  iterate over rules and create each rule.


def validate(definition: dict, schema: dict):
    print(definition)

    jsonschema.validate(instance=definition, schema=schema)

