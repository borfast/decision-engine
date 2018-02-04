# coding=utf-8
from decision_engine.comparisons import Comparison
from decision_engine.sources import Source


class Rule:
    def __init__(self, source1: Source, source2: Source,
                 comparison: Comparison) -> None:
        self.source1 = source1
        self.source2 = source2
        self.comparison = comparison

    def check(self, data: dict) -> bool:
        val1 = self.source1.get_value(data)
        val2 = self.source2.get_value(data)
        return self.comparison.check(val1, val2)
