from abc import ABC

from lox_interpreter.lox.token_type import TokenType

class Expression(ABC):
    pass

class Binary(Expression):
    def __init__(self, left: Expression, operator: TokenType, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right