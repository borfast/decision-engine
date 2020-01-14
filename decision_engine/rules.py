from abc import ABC, abstractmethod
from typing import List

from pydantic.dataclasses import dataclass

from decision_engine.comparisons import Comparison
from decision_engine.sources import Source


@dataclass
class Rule(ABC):
    name: str

    @abstractmethod
    def check(self, data: dict) -> bool:
        raise NotImplementedError  # pragma: no cover


@dataclass
class SimpleComparisonRule(Rule):
    source1: Source
    source2: Source
    comparison: Comparison

    def check(self, data: dict) -> bool:
        val1 = self.source1.get_value(data)
        val2 = self.source2.get_value(data)
        return self.comparison.check(val1, val2)


@dataclass
class BooleanOrRule(Rule):
    rules: List[Rule]

    def check(self, data: dict) -> bool:
        return any([rule.check(data) for rule in self.rules])


@dataclass
class BooleanAndRule(Rule):
    rules: List[Rule]

    def check(self, data: dict) -> bool:
        return all([rule.check(data) for rule in self.rules])
