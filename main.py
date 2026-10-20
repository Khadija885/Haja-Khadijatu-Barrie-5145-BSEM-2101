class Stack:
    """A simple stack data structure."""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            raise ValueError("Stack is empty")
        return self.items.pop()

    def peek(self):
        if not self.items:
            raise ValueError("Stack is empty")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


def tokenize(expression):
    """Separate numbers, operators and parentheses."""
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit() or char == ".":
            start = i
            dots = 0

            while i < len(expression) and (
                expression[i].isdigit()
                or expression[i] == "."
            ):
                if expression[i] == ".":
                    dots += 1
                i += 1

            if dots > 1:
                raise ValueError("Invalid number")

            number = expression[start:i]
            tokens.append(float(number))
            continue

        if char in "+-*/()":
            tokens.append(char)
            i += 1
            continue

        raise ValueError(f"Invalid character: {char}")

    return tokens


def evaluate_expression(expression):
    """Evaluate an expression using two stacks."""
    values = Stack()
    operators = Stack()

    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2
    }

    tokens = tokenize(expression)
    expecting_number = True

    def apply_operator():
        operator = operators.pop()
        right = values.pop()
        left = values.pop()

        if operator == "+":
            result = left + right
        elif operator == "-":
            result = left - right
        elif operator == "*":
            result = left * right
        else:
            if right == 0:
                raise ZeroDivisionError(
                    "Division by zero"
                )
            result = left / right

        values.push(result)

    for token in tokens:
        if isinstance(token, float):
            if not expecting_number:
                raise ValueError("Missing operator")
            values.push(token)
            expecting_number = False

        elif token == "(":
            if not expecting_number:
                raise ValueError("Missing operator")
            operators.push(token)

        elif token == ")":
            if expecting_number:
                raise ValueError("Invalid parentheses")

            while (
                not operators.is_empty()
                and operators.peek() != "("
            ):
                apply_operator()

            if operators.is_empty():
                raise ValueError("Mismatched parentheses")

            operators.pop()
            expecting_number = False

        elif token in "+-*/":
            if expecting_number:
                if token in "+-":
                    values.push(0.0)
                else:
                    raise ValueError("Invalid expression")

            while (
                not operators.is_empty()
                and operators.peek() != "("
                and precedence[operators.peek()]
                >= precedence[token]
            ):
                apply_operator()

            operators.push(token)
            expecting_number = True

    if not tokens or expecting_number:
        raise ValueError("Incomplete expression")

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("Mismatched parentheses")
        apply_operator()

    if len(values.items) != 1:
        raise ValueError("Invalid expression")

    return values.pop()


def main():
    input_file = "input.txt"
    output_file = "output.txt"
    separator = "-----"

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()

        # Each separator ends one expression group.
        groups = []
        current_group = []

        for line in content.splitlines():
            if line.strip() == separator:
                groups.append(current_group)
                current_group = []
            else:
                current_group.append(line)

        if current_group or not groups:
            groups.append(current_group)

        output_groups = []

        for group in groups:
            results = []

            for expression in group:
                if not expression.strip():
                    continue

                try:
                    result = evaluate_expression(expression)

                    if result.is_integer():
                        results.append(str(int(result)))
                    else:
                        results.append(
                            f"{result:.10g}"
                        )

                except (ValueError, ZeroDivisionError) as error:
                    results.append(f"Error: {error}")

            output_groups.append(results)

        with open(output_file, "w", encoding="utf-8") as file:
            for index, group in enumerate(output_groups):
                for result in group:
                    file.write(result + "\n")

                if index < len(output_groups) - 1:
                    file.write(separator + "\n")

        print("Evaluation completed.")
        print(f"Results saved in {output_file}.")

    except FileNotFoundError:
        print("Error: input.txt was not found.")


if __name__ == "__main__":
    main()