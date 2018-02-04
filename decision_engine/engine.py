# coding=utf-8
from typing import List

from decision_engine.rules import Rule


class Engine:
    rules: List = []

    def __init__(self, rules: List[Rule]) -> None:
        self.rules = rules

    def decide(self, data: dict) -> bool:
        return all([rule.check(data) for rule in self.rules])
