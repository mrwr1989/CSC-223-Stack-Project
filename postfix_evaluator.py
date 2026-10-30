
"""Evaluate postfix expressions using the Stack class."""

from stack import Stack


class PostfixEvaluator:
    """Evaluate numeric postfix expressions."""

    def evaluate(self, expression):
        """Return the result of a postfix expression."""
        operands = Stack()
        operators = {"+", "-", "*", "/"}

        tokens = expression.split()

        if not tokens:
            raise ValueError("Empty expression")

        for token in tokens:
            if token in operators:
                if operands.size() < 2:
                    raise ValueError("Insufficient operands")

                right = operands.pop()
                left = operands.pop()

                if token == "+":
                    result = left + right
                elif token == "-":
                    result = left - right
                elif token == "*":
                    result = left * right
                else:
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = left / right

                operands.push(result)
            else:
                try:
                    number = float(token)
                except ValueError:
                    raise ValueError(
                        f"Invalid token: {token}"
                    )
                operands.push(number)

        if operands.size() != 1:
            raise ValueError("Malformed postfix expression")

        return operands.pop()



if __name__ == "__main__":
    evaluator = PostfixEvaluator()

    # Test basic arithmetic
    assert evaluator.evaluate("5 3 +") == 8
    assert evaluator.evaluate("8 2 - 3 +") == 9
    assert evaluator.evaluate("5 3 8 * +") == 29
    assert evaluator.evaluate("6 2 / 3 +") == 6
    print("Basic arithmetic tests passed")

    # Test operand order and multi-digit numbers
    assert evaluator.evaluate("8 2 -") == 6
    assert evaluator.evaluate("8 2 /") == 4
    assert evaluator.evaluate("35 27 + 3 *") == 186
    print("Operand order and multi-digit tests passed")

    # Test invalid expressions
    for expression in ["5 +", "2 3 4 +", "3 4 &"]:
        try:
            evaluator.evaluate(expression)
            raise AssertionError("Expected ValueError")
        except ValueError:
            pass
    print("Invalid expression tests passed")

    # Test division by zero
    try:
        evaluator.evaluate("8 0 /")
        raise AssertionError("Expected ZeroDivisionError")
    except ZeroDivisionError:
        print("Division by zero test passed")

    print("All Postfix Evaluator tests passed!")
