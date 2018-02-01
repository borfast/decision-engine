# coding=utf-8
from abc import ABC, abstractmethod


class Comparison(ABC):
    @abstractmethod
    def check(self, x: any, y: any) -> bool:
        pass


class Equal(Comparison):
    def check(self, x: any, y: any) -> bool:
        return x == y


class GreaterThan(Comparison):
    def check(self, x: any, y: any) -> bool:
        return x > y


class GreaterThanOrEqual(Comparison):
    def check(self, x: any, y: any) -> bool:
        return x >= y


class LessThan(Comparison):
    def check(self, x: any, y: any) -> bool:
        return x < y


class LessThanOrEqual(Comparison):
    def check(self, x: any, y: any) -> bool:
        return x <= y
