import tkinter as tk
from view import CalculatorView


def main():
    root = tk.Tk()
    CalculatorView(root)
    root.mainloop()


if __name__ == "__main__":
    main()