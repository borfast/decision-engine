# coding=utf-8
from typing import List

from decision_engine.rules import Rule


class Engine:
    rules: List = []

    def __init__(self, rules: List[Rule], name: str = None) -> None:
        self.rules = rules
        self.name = name

    def decide(self, data: dict) -> bool:
        return all([rule.check(data) for rule in self.rules])
