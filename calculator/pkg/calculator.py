# calculator.py

class Calculator:
    def __init__(self):
        # A dictionary mapping operator strings to functions (using lambda for brevity)
        # Lambda functions are small, anonymous functions defined inline.
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        # Define operator precedence (order of operations)
        # Higher number means it happens first (multiplication/division before addition/subtraction)
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        """
        Evaluate a mathematical expression string.
        """
        if not expression or expression.isspace():
            return None
        # Split the string by whitespace into a list of tokens (numbers and operators)
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        """
        Internal method to evaluate tokens using two stacks: one for numbers, one for operators.
        """
        values = []     # Stack to store numbers
        operators = []  # Stack to store operators

        for token in tokens:
            if token in self.operators:
                # If it's an operator, we need to respect precedence.
                # If the top of the operator stack has higher or equal precedence,
                # apply it first.
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                # If it's not an operator, assume it's a number
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        # Apply any remaining operators
        while operators:
            self._apply_operator(operators, values)

        # The final result should be the only item left in the values stack
        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        """
        Helper to pop an operator and two values, calculate the result, and push it back.
        """
        if not operators:
            return

        operator = operators.pop() # Remove the last operator
        
        # We need at least two numbers to perform an operation (e.g., a + b)
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop() # The second operand (right side)
        a = values.pop() # The first operand (left side)
        
        # Look up the function in our dictionary and call it
        values.append(self.operators[operator](a, b))
