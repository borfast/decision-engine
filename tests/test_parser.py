from pathlib import Path

from decision_engine import parser


def test_three_sections_are_read():
    file_name = 'test_definition.json'
    definition_path = (Path(__file__).parents[0] / file_name).absolute()
    definition: dict = parser.parse_from_file(definition_path)

    assert 'sources' in definition
    assert 'rules' in definition
    assert 'engines' in definition
