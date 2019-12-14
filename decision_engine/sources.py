# coding=utf-8
import random
from typing import Optional, Any

from abc import ABC, abstractmethod


class Source(ABC):
    @abstractmethod
    def __init__(self, name: str = None):
        self.name = name

    def get_value(self, data: Optional[dict] = None) -> Any:
        pass


class DictSource(Source):
    def __init__(self, key: str, name: str = None) -> None:
        self.key = key
        super().__init__(name)

    def get_value(self, data: Optional[dict] = None) -> Any:
        if data is None:
            return None
        return data[self.key]


class FixedValueSource(Source):
    def __init__(self, value: Any, name: str = None) -> None:
        self.value: Any = value
        super().__init__(name)

    def get_value(self, data: Optional[dict] = None) -> Any:
        return self.value


class PercentageSource(Source):
    def __init__(self, percentage: float, source: Source, name: str = None) -> None:
        self.percentage = float(percentage)
        self.source = source
        super().__init__(name)

    def get_value(self, data: Optional[dict] = None) -> float:
        return self.source.get_value(data) * self.percentage


class RandomIntSource(Source):
    def __init__(self, min_value: int, max_value: int, seed: int = None, name: str = None):
        self.min_value = min_value
        self.max_value = max_value
        self.seed = seed
        super().__init__(name)

    def get_value(self, data: Optional[dict] = None):
        if self.seed is not None:
            random.seed(self.seed)

        return random.randint(self.min_value, self.max_value)
