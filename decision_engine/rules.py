# coding=utf-8
from abc import abstractmethod

from decision_engine.comparisons import Comparison
from decision_engine.sources import Source


class Rule:
    def __init__(self, name: str = None):
        self.name = name

    @abstractmethod
    def check(self, data: dict) -> bool:
        pass


class SimpleRule(Rule):
    def __init__(self, source1: Source, source2: Source,
                 comparison: Comparison, name: str = None) -> None:
        self.source1 = source1
        self.source2 = source2
        self.comparison = comparison
        super().__init__(name)

    def check(self, data: dict) -> bool:
        val1 = self.source1.get_value(data)
        val2 = self.source2.get_value(data)
        return self.comparison.check(val1, val2)


class BooleanOrRule(Rule):
    def __init__(self, rule1: Rule, rule2: Rule, name: str = None) -> None:
        self.rule1 = rule1
        self.rule2 = rule2
        super().__init__(name)

    def check(self, data: dict) -> bool:
        return self.rule1.check(data) or self.rule2.check(data)


class BooleanAndRule(Rule):
    def __init__(self, rule1: Rule, rule2: Rule, name: str = None) -> None:
        self.rule1 = rule1
        self.rule2 = rule2
        super().__init__(name)

    def check(self, data: dict) -> bool:
        return self.rule1.check(data) and self.rule2.check(data)
