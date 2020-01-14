from typing import Any

from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass


@dataclass
class Comparison(ABC):
    @abstractmethod
    def check(self, x: Any, y: Any) -> bool:  # pragma: no cover
        raise NotImplementedError


@dataclass
class NoOp(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return True


@dataclass
class Equal(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x == y


@dataclass
class NotEqual(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x != y


@dataclass
class GreaterThan(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x > y


@dataclass
class GreaterThanOrEqual(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x >= y


@dataclass
class LessThan(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x < y


@dataclass
class LessThanOrEqual(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x <= y
