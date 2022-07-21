import unittest

from interpreter import *


class EnvironmentTest(unittest.TestCase):
    def test_token_values(self):
        self.assertEqual(Number(3).value, 3)
        self.assertEqual(Number(3.1).value, 3.1)
        self.assertEqual(Variable('var').symbol, 'var')


class TokenizerTest(unittest.TestCase):
    def test_tokenizer(self):
        expression = '-8*x+-12^(-y-2.7)/z'
        self.assertEqual(Tokenizer(expression).get_tokens(),
                         deque([UNARY_OPERATORS['-'], Number(8), BINARY_OPERATORS['*'],
                                Variable('x'), BINARY_OPERATORS['+'], UNARY_OPERATORS['-'], Number(12),
                                BINARY_OPERATORS['^'], Token('('), UNARY_OPERATORS['-'], Variable('y'),
                                BINARY_OPERATORS['-'], Number(2.7), Token(')'), BINARY_OPERATORS['/'],
                                Variable('z')]))

    def test_is_unary_operator(self):
        self.assertEqual(is_unary_operator('+', None), True)
        self.assertEqual(is_unary_operator('+', BINARY_OPERATORS['+']), True)
        self.assertEqual(is_unary_operator('+', Token('(')), True)
        self.assertEqual(is_unary_operator('*', None), False)
        self.assertEqual(is_unary_operator('*', BINARY_OPERATORS['+']), False)
        self.assertEqual(is_unary_operator('*', Token('(')), False)

    def test_InvalidToken(self):
        expression = '3 + 4j'
        with self.assertRaises(InvalidToken):
            Tokenizer(expression).get_tokens()


class ConverterTest(unittest.TestCase):
    def test_normal_operators(self):
        expression = '8 * x + 12 ^ (y - 2.7) / z'
        tokens = Tokenizer(expression).get_tokens()
        postfix_expression = Converter(tokens).get_postfix_expression()
        self.assertEqual(postfix_expression, '8 x * 12 y 2.7 - ^ z / +')

    def test_unary_operators(self):
        expression = '- - 1'
        tokens = Tokenizer(expression).get_tokens()
        postfix_expression = Converter(tokens).get_postfix_expression()
        self.assertEqual(postfix_expression, '1 - -')

    def test_MissingRightParenthesis(self):
        expression = '(2+3'
        tokens = Tokenizer(expression).get_tokens()
        with self.assertRaises(MissingParenthesis):
            Converter(tokens).get_postfix_expression()

    def test_MissingLeftParenthesis(self):
        expression = '2+3)'
        tokens = Tokenizer(expression).get_tokens()
        with self.assertRaises(MissingParenthesis):
            Converter(tokens).get_postfix_expression()

    def test_UnexpectedAssignment(self):
        expression = 'a=3'
        tokens = Tokenizer(expression).get_tokens()
        with self.assertRaises(UnexpectedAssignment):
            Converter(tokens).get_postfix_expression()


class InterpreterTest(unittest.TestCase):
    def test_normal_operators(self):
        expression = '8 * 5 + 12 ^ (1 - 2.7) / -1'
        self.assertAlmostEqual(Interpreter(expression).evaluate(), 39.985365, places=6)

    def test_unary_operators(self):
        expression = '1 +++ 2 * 3 -- 4'
        self.assertEqual(Interpreter(expression).evaluate(), 11)

    def test_UnknownVariable(self):
        expression = 'a+1'
        with self.assertRaises(UnknownVariable):
            Interpreter(expression).evaluate()

    def test_InvalidExpression(self):
        expression = '3 *** 5'
        with self.assertRaises(InvalidExpression):
            Interpreter(expression).evaluate()


if __name__ == '__main__':
    unittest.main()
