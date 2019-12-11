import json

# TODO: validate that each engine name is unique,
#  iterate over sources and create each Source,
#  iterate over rules and create each rule.


def parse_from_file(file_path: str) -> dict:
    with (open(file_path)) as fp:
        definition = json.load(fp)

    return definition
