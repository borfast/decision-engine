# coding=utf-8
import random
from typing import Optional, Any

from abc import ABC, abstractmethod


class Source(ABC):
    @abstractmethod
    def get_value(self, data: Optional[dict] = None) -> Any:
        pass


class DictSource(Source):
    def __init__(self, key: str) -> None:
        self.key = key

    def get_value(self, data: Optional[dict] = None) -> Any:
        if data is None:
            return None
        return data[self.key]


class FixedValueSource(Source):
    def __init__(self, value: Any) -> None:
        self.value: Any = value

    def get_value(self, data: Optional[dict] = None) -> Any:
        return self.value


class PercentageSource(Source):
    def __init__(self, percentage: float, source: Source) -> None:
        self.percentage = float(percentage)
        self.source = source

    def get_value(self, data: Optional[dict] = None) -> float:
        return self.source.get_value(data) * self.percentage


class RandomIntSource(Source):
    def __init__(self, min_value: int, max_value: int, seed: int = None):
        self.min_value = min_value
        self.max_value = max_value
        self.seed = seed

    def get_value(self, data: Optional[dict] = None):
        if self.seed is not None:
            random.seed(self.seed)

        return random.randint(self.min_value, self.max_value)
