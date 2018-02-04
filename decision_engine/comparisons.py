# coding=utf-8
from typing import Any

from abc import ABC, abstractmethod


class Comparison(ABC):
    @abstractmethod
    def check(self, x: Any, y: Any) -> bool:
        pass


class Equal(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x == y


class NotEqual(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x != y


class GreaterThan(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x > y


class GreaterThanOrEqual(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x >= y


class LessThan(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x < y


class LessThanOrEqual(Comparison):
    def check(self, x: Any, y: Any) -> bool:
        return x <= y
