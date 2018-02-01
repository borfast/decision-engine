# coding=utf-8
from abc import ABC, abstractmethod


class Source(ABC):
    @abstractmethod
    def get_value(self, data: dict = None) -> any:
        pass


class DictSource(Source):
    def __init__(self, key: str):
        self.key = key

    def get_value(self, data: dict = None) -> any:
        return data[self.key]


class FixedValueSource(Source):
    def __init__(self, value: any):
        self.value = value

    def get_value(self, data: dict = None) -> any:
        return self.value


class PercentageSource(Source):
    def __init__(self, percentage: float, source: Source):
        self.percentage = float(percentage)
        self.source = source

    def get_value(self, data: dict = None) -> float:
        return self.source.get_value(data) * self.percentage
