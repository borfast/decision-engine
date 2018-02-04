# coding=utf-8
from abc import abstractmethod

from decision_engine.comparisons import Comparison
from decision_engine.sources import Source


class Rule:
    @abstractmethod
    def check(self, data: dict) -> bool:
        pass


class SimpleRule(Rule):
    def __init__(self, source1: Source, source2: Source,
                 comparison: Comparison) -> None:
        self.source1 = source1
        self.source2 = source2
        self.comparison = comparison

    def check(self, data: dict) -> bool:
        val1 = self.source1.get_value(data)
        val2 = self.source2.get_value(data)
        return self.comparison.check(val1, val2)


class BooleanOrRule(Rule):
    def __init__(self, rule1: Rule, rule2: Rule) -> None:
        self.rule1 = rule1
        self.rule2 = rule2

    def check(self, data: dict) -> bool:
        return self.rule1.check(data) or self.rule2.check(data)


class BooleanAndRule(Rule):
    def __init__(self, rule1: Rule, rule2: Rule) -> None:
        self.rule1 = rule1
        self.rule2 = rule2

    def check(self, data: dict) -> bool:
        return self.rule1.check(data) and self.rule2.check(data)
