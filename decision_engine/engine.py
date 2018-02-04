# coding=utf-8
# from decision_engine.comparisons import Comparison
from typing import List

from decision_engine.rules import Rule


class Engine:
    rules: List = []

    def __init__(self, rules: List[Rule]) -> None:
        self.rules = rules

    # def add_rule(self, rule: Comparison, operator: str):
    #     self.rules

    def decide(self, data: dict) -> bool:
        # TODO: For now this is basically an all AND or else it fails.
        for rule in self.rules:
            if not rule.check(data):
                return False

        return True
