from abc import ABC, abstractmethod
from typing import List

from decision_engine.comparisons import Comparison
from decision_engine.sources import Source


class Rule(ABC):
    def __init__(self, name: str = None):
        self.name = name

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def check(self, data: dict) -> bool:
        raise NotImplementedError  # pragma: no cover


class SimpleComparisonRule(Rule):
    def __init__(self, source1: Source, source2: Source,
                 comparison: Comparison, name: str = None) -> None:
        self.source1 = source1
        self.source2 = source2
        self.comparison = comparison
        super().__init__(name)

    def __repr__(self):
        return f"Name: '{self.name}' | source1: '{self.source1.name}' | " \
               f"source2: '{self.source2.name}' | " \
               f"comparison: '{self.comparison.__class__.__name__}'"

    def check(self, data: dict) -> bool:
        val1 = self.source1.get_value(data)
        val2 = self.source2.get_value(data)
        return self.comparison.check(val1, val2)


class BooleanOrRule(Rule):
    def __init__(self, rules: List[Rule], name: str = None) -> None:
        self.rules = rules
        super().__init__(name)

    def __repr__(self):
        return f"Name: '{self.name}' | rules: {self.rules}"

    def check(self, data: dict) -> bool:
        return any([rule.check(data) for rule in self.rules])


class BooleanAndRule(Rule):
    def __init__(self, rules: List[Rule], name: str = None) -> None:
        self.rules = rules
        super().__init__(name)

    def __repr__(self):
        return f"Name: '{self.name}' | rules: {self.rules}"

    def check(self, data: dict) -> bool:
        return all([rule.check(data) for rule in self.rules])
