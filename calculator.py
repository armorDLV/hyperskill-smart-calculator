from interpreter import *


def main():
    while True:
        user_input = input().strip()
        if user_input == '':
            continue
        if user_input == '/exit':
            print('Bye!')
            return
        elif user_input == '/help':
            print('Calculator for simple mathematical expressions:\n',
                  '- Input an _expression to evaluate it\n',
                  '- To define a variable type "varname = string" (varname must be alphabetic)\n',
                  '- Supported operators: ' + ' '.join(SYMBOLS))
        elif user_input.startswith('/'):
            print('Unknown command')
        elif '=' in user_input:
            try_evaluate_variable_declaration(user_input)
        else:
            try_evaluate(user_input)


def try_evaluate(user_input) -> None:
    try:
        print(int(Interpreter(user_input).evaluate()))
    except Exception as e:
        print(e)


def try_evaluate_variable_declaration(user_input):
    try:
        evaluate_variable_declaration(user_input)
    except Exception as e:
        print(e)


def evaluate_variable_declaration(expression: str):
    variable_name, sub_expression = expression.split('=', maxsplit=1)
    variable_name = variable_name.strip()
    if not variable_name.isalpha():
        raise InvalidAssignment()
    else:
        variables[variable_name] = Number(Interpreter(sub_expression).evaluate())


class InvalidAssignment(Exception):
    def __init__(self):
        super().__init__(f'Calculator: invalid identifier')


if __name__ == '__main__':
    main()
