import operator as op
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Token:
    symbol: str

    def __repr__(self):
        return self.symbol


@dataclass
class Number(Token):
    value: int | float

    def __init__(self, number: int | float):
        self.symbol = str(number)
        self.value = number

    def __repr__(self):
        return f'N({self.value})'


@dataclass
class Variable(Token):
    def __repr__(self):
        return f'V({self.symbol})'


@dataclass
class Operator(Token):
    action: Any
    precedence: int
    associativity: str


@dataclass
class BinaryOperator(Operator):
    action: Callable[[Any, Any], int | float]

    def __repr__(self):
        return f'B({self.symbol})'


@dataclass
class UnaryOperator(Operator):
    action: Callable[[Any], int | float]

    def __repr__(self):
        return f'U({self.symbol})'


UNARY_OPERATORS: dict[str: UnaryOperator] = dict()
UNARY_OPERATORS['+'] = UnaryOperator('+', op.pos, 4, 'none')
UNARY_OPERATORS['-'] = UnaryOperator('-', op.neg, 4, 'none')

BINARY_OPERATORS: dict[str: BinaryOperator] = dict()
BINARY_OPERATORS['+'] = BinaryOperator('+', op.add, 1, 'left')
BINARY_OPERATORS['-'] = BinaryOperator('-', op.sub, 1, 'left')
BINARY_OPERATORS['*'] = BinaryOperator('*', op.mul, 2, 'left')
BINARY_OPERATORS['/'] = BinaryOperator('/', op.truediv, 2, 'left')
BINARY_OPERATORS['^'] = BinaryOperator('^', op.pow, 3, 'right')

SYMBOLS = set(BINARY_OPERATORS) | {'(', ')', '='}

variables: dict[str: Number] = {}
