from tokenizer import *


class Converter:
    def __init__(self, infix_expression: deque[Token]):
        self._input = infix_expression
        self._output = deque()
        self._stack = deque()
        self._convert()

    # https://www.andr.mu/logs/the-shunting-yard-algorithm/
    def _convert(self) -> None:
        while self._there_are_tokens():
            token = self._pop_from_input()
            if isinstance(token, (Number, Variable)):
                self._push_to_output(token)
            elif isinstance(token, UnaryOperator):
                self._push_to_stack(token)
            elif isinstance(token, BinaryOperator):
                if token.associativity == 'left':
                    while self._operator_in_stack_has_higher_or_equal_precedence_than(token):
                        self._move_token_from_stack_to_output()
                    self._push_to_stack(token)
                elif token.associativity == 'right':
                    while self._operator_in_stack_has_higher_precedence_than(token):
                        self._move_token_from_stack_to_output()
                    self._push_to_stack(token)
            elif token.symbol in '(':
                self._push_to_stack(token)
            elif ')' == token.symbol:
                while self._no_left_parenthesis_on_top_of_stack():
                    self._move_token_from_stack_to_output()
                if len(self._stack) == 0:
                    raise MissingParenthesis()  # missing )
                else:
                    self._pop_stack()  # discard the matching '('
            else:
                raise UnexpectedAssignment()

        while len(self._stack) > 0:
            if isinstance(operator := self._pop_stack(), Operator):
                self._push_to_output(operator)
            else:
                raise MissingParenthesis()  # missing (

    def _there_are_tokens(self) -> bool:
        return len(self._input) > 0

    def _pop_from_input(self) -> Token:
        return self._input.popleft()

    def _push_to_output(self, token) -> None:
        self._output.append(token)

    def _operator_in_stack_has_higher_or_equal_precedence_than(self, token) -> bool:
        return len(self._stack) > 0 and isinstance(self._peek_stack(), Operator) \
               and self._peek_stack().precedence >= token.precedence

    def _operator_in_stack_has_higher_precedence_than(self, token) -> bool:
        return len(self._stack) > 0 and isinstance(self._peek_stack(), Operator) \
               and self._peek_stack().precedence > token.precedence

    def _move_token_from_stack_to_output(self) -> None:
        self._push_to_output(self._pop_stack())

    def _push_to_stack(self, token) -> None:
        self._stack.append(token)

    def _pop_stack(self) -> Operator | Token:
        return self._stack.pop()

    def _no_left_parenthesis_on_top_of_stack(self):
        return len(self._stack) > 0 and self._peek_stack().symbol != '('

    def _peek_stack(self) -> Operator | Token:
        return self._stack[-1]

    def get_postfix_tokens(self) -> deque[Token]:
        return self._output

    def get_postfix_expression(self) -> str:
        token_values = [token.symbol for token in self._output]
        return ' '.join(token_values)


class MissingParenthesis(Exception):
    def __init__(self):
        super().__init__('Invalid expression')


class UnexpectedAssignment(Exception):
    def __init__(self):
        super().__init__('Invalid assignment')


if __name__ == '__main__':
    while (expr := input()) != '/exit':
        try:
            _infix_tokens = Tokenizer(expr).get_tokens()
            print(Converter(_infix_tokens).get_postfix_expression())
        except Exception as err:
            print(err)
