from collections import deque

from environment import *


class Tokenizer:
    def __init__(self, expression: str):
        self._expression = expression
        self._atoms = self._get_atoms()
        self._typed_tokens = self._get_typed_tokens()

    # This approach is valid only when all symbols are single character
    def _get_atoms(self) -> list[str]:
        for symbol in SYMBOLS:
            self._expression = self._expression.replace(symbol, f' {symbol} ')
        return self._expression.split()

    def _get_typed_tokens(self) -> deque[Token]:
        output = deque()

        for atom in self._atoms:
            if number := get_number_or_none(atom):
                output.append(Number(number))
            elif atom in BINARY_OPERATORS:
                previous_token = output[-1] if output else None
                output.append(get_operator(atom, previous_token))
            elif atom in {'(', ')', '='}:
                output.append(Token(atom))
            elif atom.isalpha():
                output.append(Variable(atom))
            else:
                raise InvalidToken()

        return output

    def get_tokens(self) -> deque[Token]:
        return self._typed_tokens

    def print_tokens(self):
        print(*[token.__repr__() for token in self._typed_tokens])


def get_number_or_none(atom: str) -> int | float | None:
    for number_type in (int, float):
        try:
            return number_type(atom)
        except ValueError:
            pass
    return None


def get_operator(atom: str, previous_token: Token | None):
    return UNARY_OPERATORS[atom] if is_unary_operator(atom, previous_token) else BINARY_OPERATORS[atom]


def is_unary_operator(atom: str, previous_token: Token | None) -> bool:
    if atom in UNARY_OPERATORS:
        return previous_token is None or isinstance(previous_token, Operator) or previous_token.symbol == '('
    else:
        return False


class InvalidToken(Exception):
    def __init__(self):
        super().__init__('Invalid identifier')


if __name__ == '__main__':
    while (expr := input()) != '/exit':
        try:
            Tokenizer(expr).print_tokens()
        except Exception as err:
            print(err)
