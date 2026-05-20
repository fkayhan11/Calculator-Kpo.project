from tkinter import messagebox
from model import CalculatorModel


class CalculatorController:
    """
    CONTROLLER: Processes user input and connects View with Model
    """

    def __init__(self, view):
        self.model = CalculatorModel()
        self.view = view
        self.update_display()

    def update_display(self):
        self.view.set_display(self.model.get_display())
        if hasattr(self.view, "set_operation_count"):
            try:
                self.view.set_operation_count(self.model.get_operation_count())
            except Exception:
                pass

    def handle_input(self, value: str):
        try:
            if value.isdigit():
                self.model.input_digit(value)

            elif value == ".":
                self.model.input_decimal()

            elif value in ["+", "-", "/", "x"]:
                operator = "*" if value == "x" else value
                self.model.set_operator(operator)

            elif value == "=":
                self.model.calculate()

            elif value == "C":
                self.model.clear()

            elif value == "⌫":
                self.model.backspace()

            elif value == "%":
                self.model.percentage()

            elif value == "√":
                self.model.square_root()

            elif value == "x²":
                self.model.square()

            elif value == "±":
                self.model.toggle_sign()

            elif value == "MC":
                self.model.memory_clear()

            elif value == "MR":
                self.model.memory_recall()

            elif value == "M+":
                self.model.memory_add()

            elif value == "M-":
                self.model.memory_subtract()

            self.update_display()

        except Exception as exc:
            msg = str(exc).strip()
            if not msg or len(msg) > 120:
                msg = "Invalid operation."
            messagebox.showerror("Error", msg)
            self.model.clear()
            self.update_display()

    def handle_keyboard(self, char: str):
        if char in "0123456789":
            self.handle_input(char)
        elif char in "+-/":
            self.handle_input(char)
        elif char == "*":
            self.handle_input("x")
        elif char == ".":
            self.handle_input(char)
        elif char == "%":
            self.handle_input(char)
        elif char in ("c", "C"):
            self.handle_input("C")
        elif char in ("=", "\r", "\n"):
            self.handle_input("=")
        elif char in ("r", "R"):
            self.handle_input("√")
        elif char in ("q", "Q"):
            self.handle_input("x²")
        elif char in ("n", "N"):
            self.handle_input("±")
        elif char in ("m", "M"):
            self.handle_input("MR")
