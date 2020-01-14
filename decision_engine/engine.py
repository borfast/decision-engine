# coding=utf-8
from typing import List

from pydantic.dataclasses import dataclass

from decision_engine.rules import Rule


@dataclass
class Engine:
    name: str
    rules: List[Rule]

    def decide(self, data: dict) -> bool:
        return all([rule.check(data) for rule in self.rules])
