
"""Convert infix expressions to postfix using a stack."""

import re
from stack import Stack


class InfixToPostfixConverter:
    """Convert arithmetic expressions using the shunting-yard algorithm."""

    def __init__(self):
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    def convert(self, expression):
        """Convert an infix expression to postfix notation."""
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Empty expression")

        tokens = re.findall(r"[A-Za-z]+|\d+(?:\.\d+)?|[()+*/-]|\S", expression)
        output = []
        operators = Stack()
        expecting_operand = True

        for token in tokens:
            is_operand = bool(re.fullmatch(r"[A-Za-z]+|\d+(?:\.\d+)?", token))

            if is_operand:
                if not expecting_operand:
                    raise ValueError("Misplaced operand")
                output.append(token)
                expecting_operand = False

            elif token == "(":
                if not expecting_operand:
                    raise ValueError("Missing operator before '('")
                operators.push(token)

            elif token == ")":
                if expecting_operand:
                    raise ValueError("Misplaced ')' or incomplete expression")

                while not operators.is_empty() and operators.peek() != "(":
                    output.append(operators.pop())

                if operators.is_empty():
                    raise ValueError("Mismatched parentheses")

                operators.pop()
                expecting_operand = False

            elif token in self.precedence:
                if expecting_operand:
                    raise ValueError("Misplaced operator")

                while (not operators.is_empty()
                       and operators.peek() in self.precedence
                       and self.precedence[operators.peek()] >= self.precedence[token]):
                    output.append(operators.pop())

                operators.push(token)
                expecting_operand = True

            else:
                raise ValueError(f"Invalid token: {token}")

        if expecting_operand:
            raise ValueError("Incomplete expression")

        while not operators.is_empty():
            operator = operators.pop()
            if operator == "(":
                raise ValueError("Mismatched parentheses")
            output.append(operator)

        return " ".join(output)

        
if __name__ == "__main__":
    converter = InfixToPostfixConverter()

    # Test basic expressions and precedence
    assert converter.convert("A + B") == "A B +"
    assert converter.convert("A + B * C") == "A B C * +"
    assert converter.convert("(A + B) * C") == "A B + C *"
    print("Basic conversion tests passed")

    # Test parentheses and complex expressions
    assert converter.convert("A * B + C / D") == "A B * C D / +"
    assert converter.convert("(A + B) * (C - D)") == "A B + C D - *"
    assert converter.convert("A + B * C - D / E") == "A B C * + D E / -"
    assert converter.convert("A * (B + C) / D") == "A B C + * D /"
    assert converter.convert("(A + B * C) / (D - E)") == "A B C * + D E - /"
    assert converter.convert("A + (B - C) * D") == "A B C - D * +"
    assert converter.convert("(A + B * (C - D)) / E") == "A B C D - * + E /"
    print("Complex conversion tests passed")

    # Test equal precedence and left associativity
    assert converter.convert("A - B + C") == "A B - C +"
    assert converter.convert("A / B * C") == "A B / C *"
    print("Operator precedence tests passed")

    # Test malformed expressions
    invalid = ["A+B)", "(A+B", "A+*B", "+AB", "A+B;C", "A+B/"]
    for expression in invalid:
        try:
            converter.convert(expression)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected error for: {expression}")
    print("Invalid expression tests passed")

    print("All Infix Converter tests passed!")

