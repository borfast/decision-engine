# coding=utf-8
import random
from typing import Optional, Any

from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass


@dataclass
class Source(ABC):
    name: str

    @abstractmethod
    def get_value(self, data: Optional[dict] = None) -> Any:
        raise NotImplementedError  # pragma: no cover


@dataclass
class DictSource(Source):
    key: str

    def get_value(self, data: Optional[dict] = None) -> Any:
        if data is None:
            return None
        return data[self.key]


@dataclass
class FixedValueSource(Source):
    value: Any

    def get_value(self, data: Optional[dict] = None) -> Any:
        return self.value


@dataclass
class PercentageSource(Source):
    percentage: float
    source: Source

    def get_value(self, data: Optional[dict] = None) -> float:
        return self.source.get_value(data) * self.percentage


@dataclass
class RandomIntSource(Source):
    min_value: int
    max_value: int
    seed: Optional[int] = None

    def get_value(self, data: Optional[dict] = None) -> int:
        if self.seed is not None:
            random.seed(self.seed)

        return random.randint(self.min_value, self.max_value)
