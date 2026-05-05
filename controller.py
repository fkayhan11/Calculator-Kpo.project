from tkinter import messagebox
from model import CalculatorModel


class CalculatorController:
    """
    Controller layer of the calculator.
    Connects the model and the view.
    """

    def __init__(self, view):
        self.model = CalculatorModel()
        self.view = view
        self.update_display()

    def update_display(self):
        self.view.set_display(self.model.get_display())

    def handle_input(self, value: str):
        try:
            if value.isdigit():
                self.model.input_digit(value)

            elif value == ".":
               self.model.input_decimal()

            elif value in ["+", "-", "/", "x"]:
                if value == "x":
                    self.model.set_operator("*")
                else:
                    self.model.set_operator(value)

            elif value == "=":
                self.model.calculate()

            elif value == "C":
                self.model.clear()

            elif value == "⌫":
                self.model.backspace()


            elif value == "%":

                self.model.percentage()

            self.update_display()

        except ZeroDivisionError as error:
            messagebox.showerror("Math Error", str(error))
            self.model.clear()
            self.update_display()

        except Exception:
            messagebox.showerror("Input Error", "Invalid operation.")
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