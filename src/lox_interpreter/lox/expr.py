from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

R = TypeVar('R')

class exprVisitor(ABC, Generic[R]):
    @abstractmethod
    def visit_binary_expr(self, expr: 'Binary') -> R:
        ...

    @abstractmethod
    def visit_grouping_expr(self, expr: 'Grouping') -> R:
        ...

    @abstractmethod
    def visit_literal_expr(self, expr: 'Literal') -> R:
        ...

    @abstractmethod
    def visit_unary_expr(self, expr: 'Unary') -> R:
        ...


class expr(ABC):
    @abstractmethod
    def accept(self, visitor: 'exprVisitor[R]') -> R:
        ...

class Binary(expr):
    def __init__(self, left: Any, operator: Any, right: Any):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: 'exprVisitor[R]') -> R:
        return visitor.visit_binary_expr(self)

class Grouping(expr):
    def __init__(self, expression: Any):
        self.expression = expression

    def accept(self, visitor: 'exprVisitor[R]') -> R:
        return visitor.visit_grouping_expr(self)

class Literal(expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor: 'exprVisitor[R]') -> R:
        return visitor.visit_literal_expr(self)

class Unary(expr):
    def __init__(self, operator: Any, right: Any):
        self.operator = operator
        self.right = right

    def accept(self, visitor: 'exprVisitor[R]') -> R:
        return visitor.visit_unary_expr(self)

