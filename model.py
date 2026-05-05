from operations import Add, Subtract, Multiply, Divide


class CalculatorModel:
    """
    MODEL: Handles all business logic and calculations
    """

    def __init__(self):
        self.current_input = "0"
        self.first_operand = None
        self.operator = None
        self.reset_next = False

        # Operations dictionary (Strategy-like)
        self.operations = {
            "+": Add(),
            "-": Subtract(),
            "*": Multiply(),
            "/": Divide()
        }

    def get_display(self) -> str:
        return self.current_input

    def input_digit(self, digit: str):
        if self.reset_next:
            self.current_input = digit
            self.reset_next = False
        elif self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit

    def input_decimal(self):
        if self.reset_next:
            self.current_input = "0."
            self.reset_next = False
        elif "." not in self.current_input:
            self.current_input += "."

    def clear(self):
        self.current_input = "0"
        self.first_operand = None
        self.operator = None
        self.reset_next = False

    def backspace(self):
        if self.reset_next:
            return

        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
            if self.current_input in ["", "-"]:
                self.current_input = "0"
        else:
            self.current_input = "0"

    def percentage(self):
        current = float(self.current_input)
        result = current / 100

        if result == "Error":
            self.current_input = "Error"
        elif float(result).is_integer():
            self.current_input = str(int(result))
        else:
            self.current_input = str(result)

    def set_operator(self, operator: str):
        if self.operator and not self.reset_next:
            self.calculate()

        self.first_operand = float(self.current_input)
        self.operator = operator
        self.reset_next = True

    def calculate(self):
        if self.operator is None or self.first_operand is None:
            return

        second_operand = float(self.current_input)

        operation = self.operations.get(self.operator)

        if not operation:
            return

        result = operation.execute(self.first_operand, second_operand)

        if result == "Error":
            self.current_input = "Error"
        elif float(result).is_integer():
            self.current_input = str(int(result))
        else:
            self.current_input = str(result)

        self.first_operand = None
        self.operator = None
        self.reset_next = True