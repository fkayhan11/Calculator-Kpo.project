import tkinter as tk


class ButtonFactory:
    """
    Factory class for creating calculator buttons.
    This class applies the Factory Method idea by centralizing
    the button creation process in one place.
    """

    @staticmethod
    def create_button(parent, text, command):
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 18, "bold"),
            bd=1,
            relief="solid",
            fg="black",
            bg=ButtonFactory.get_button_color(text),
            activebackground="#dcdcdc",
            cursor="hand2",
            command=command
        )
        return button

    @staticmethod
    def get_button_color(text):
        if text in ["+", "-", "x", "/"]:
            return "#ffcc80"
        elif text == "=":
            return "#81c784"
        elif text in ["C", "⌫", "%"]:
            return "#e0e0e0"
        else:
            return "#fafafa"