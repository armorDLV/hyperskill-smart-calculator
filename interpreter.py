from converter import *


class Interpreter:
    def __init__(self, expression: str):
        self._expression = expression
        self._stack: deque[Number] = deque()
        self._infix_tokens = Tokenizer(self._expression).get_tokens()
        self._postfix_tokens = Converter(self._infix_tokens).get_postfix_tokens()

    def evaluate(self) -> int | float:
        while self._there_are_tokens():
            token = self._pop_input()
            if isinstance(token, Number):
                self._push_to_stack(token)
            elif isinstance(token, Variable):
                number = variable_to_number(token)
                self._push_to_stack(number)
            elif isinstance(token, UnaryOperator):
                number = self._evaluate_unary_operation(token)
                self._push_to_stack(number)
            elif isinstance(token, BinaryOperator):
                number = self._evaluate_binary_operation(token)
                self._push_to_stack(number)

        return self._pop_stack().value

    def _there_are_tokens(self) -> bool:
        return len(self._postfix_tokens) > 0

    def _pop_input(self) -> Token:
        return self._postfix_tokens.popleft()

    def _push_to_stack(self, token: Number) -> None:
        self._stack.append(token)

    def _pop_stack(self) -> Number:
        return self._stack.pop()

    def _evaluate_binary_operation(self, token: BinaryOperator) -> Number:
        if len(self._stack) > 1:
            b, a = self._pop_stack(), self._pop_stack()
            return Number(token.action(a.value, b.value))
        else:
            raise InvalidExpression()

    def _evaluate_unary_operation(self, token: UnaryOperator) -> Number:
        if len(self._stack) > 0:
            a = self._pop_stack()
            return Number(token.action(a.value))
        else:
            raise InvalidExpression()


def variable_to_number(var: Variable) -> Number:
    try:
        return variables[var.symbol]
    except KeyError:
        raise UnknownVariable()


class UnknownVariable(Exception):
    def __init__(self):
        super().__init__('Unknown variable')


class InvalidExpression(Exception):
    def __init__(self):
        super().__init__(f'Invalid expression')


if __name__ == '__main__':
    while (expr := input()) != '/exit':
        try:
            print(Interpreter(expr).evaluate())
        except Exception as err:
            print(err)
