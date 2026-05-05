class CalculatorModel:
    """
    This class contains the calculator logic.
    It is independent from the graphical interface.
    """

    def __init__(self):
        self.current_input = "0"
        self.first_operand = None
        self.operator = None
        self.reset_next = False

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
            if self.current_input == "-" or self.current_input == "":
                self.current_input = "0"
        else:
            self.current_input = "0"

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

        if self.operator == "+":
            result = self.first_operand + second_operand
        elif self.operator == "-":
            result = self.first_operand - second_operand
        elif self.operator == "*":
            result = self.first_operand * second_operand
        elif self.operator == "/":
            if second_operand == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result = self.first_operand / second_operand
        else:
            raise ValueError("Invalid operator.")

        if result.is_integer():
            self.current_input = str(int(result))
        else:
            self.current_input = str(result)

        self.first_operand = None
        self.operator = None
        self.reset_next = True

        def percentage(self):
            current = float(self.current_input)
            result = current / 100

            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(result)