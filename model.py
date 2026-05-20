import math
from typing import Optional

from operations import Add, Subtract, Multiply, Divide

from logging_decorator import LoggingDecorator
from history_decorator import HistoryDecorator
from file_logging_decorator import FileLoggingDecorator


class CalculatorModel:
    """
    MODEL: Handles all business logic and calculations
    """

    def __init__(self):
        self.current_input = "0"
        self.first_operand: Optional[float] = None
        self.operator: Optional[str] = None
        self.reset_next = False
        self.operation_count = 0
        self.memory_value = 0.0

        # Decorated operations using Structural Pattern (Decorator)
        self.operations = {
            "+": FileLoggingDecorator(
                LoggingDecorator(
                    HistoryDecorator(
                        Add()
                    )
                ),
                symbol="+"
            ),

            "-": FileLoggingDecorator(
                LoggingDecorator(
                    HistoryDecorator(
                        Subtract()
                    )
                )
                ,
                symbol="-"
            ),

            "*": FileLoggingDecorator(
                LoggingDecorator(
                    HistoryDecorator(
                        Multiply()
                    )
                )
                ,
                symbol="×"
            ),

            "/": FileLoggingDecorator(
                LoggingDecorator(
                    HistoryDecorator(
                        Divide()
                    )
                )
                ,
                symbol="÷"
            )
        }

    def get_display(self) -> str:
        return self.current_input

    def get_operation_count(self) -> int:
        return self.operation_count

    def _parse_current(self) -> float:
        if self.current_input == "Error":
            raise ValueError("Display is in error state")
        return float(self.current_input)

    def _format_number(self, value: float) -> str:
        if not math.isfinite(value):
            return "Error"

        # Avoid negative zero and tiny float noise.
        if abs(value) < 1e-12:
            value = 0.0

        if float(value).is_integer():
            return str(int(value))

        # 12 significant digits keeps results readable for a calculator UI.
        return format(value, ".12g")

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
        current = self._parse_current()
        result = current / 100.0
        self.current_input = self._format_number(result)

    def set_operator(self, operator: str):
        if self.operator and not self.reset_next:
            self.calculate()

        self.first_operand = float(self.current_input)
        self.operator = operator
        self.reset_next = True

    def calculate(self):
        if self.operator is None or self.first_operand is None:
            return

        second_operand = self._parse_current()

        operation = self.operations.get(self.operator)

        if not operation:
            return

        result = operation.execute(
            self.first_operand,
            second_operand
        )

        if result == "Error":
            self.current_input = "Error"
        else:
            self.current_input = self._format_number(float(result))

        self.first_operand = None
        self.operator = None
        self.reset_next = True
        self.operation_count += 1

    # Unary operations
    def square_root(self):
        value = self._parse_current()
        if value < 0:
            raise ValueError("Square root of a negative number")
        self.current_input = self._format_number(math.sqrt(value))
        self.reset_next = True
        self.operation_count += 1

    def square(self):
        value = self._parse_current()
        self.current_input = self._format_number(value * value)
        self.reset_next = True
        self.operation_count += 1

    def toggle_sign(self):
        if self.reset_next:
            # Start a new negative number after selecting an operator.
            self.current_input = "0"
            self.reset_next = False

        if self.current_input.startswith("-"):
            self.current_input = self.current_input[1:] or "0"
        else:
            if self.current_input != "0":
                self.current_input = "-" + self.current_input

    # Memory operations
    def memory_clear(self):
        self.memory_value = 0.0

    def memory_recall(self):
        self.current_input = self._format_number(self.memory_value)
        self.reset_next = True

    def memory_add(self):
        self.memory_value += self._parse_current()

    def memory_subtract(self):
        self.memory_value -= self._parse_current()
