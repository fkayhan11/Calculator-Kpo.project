import tkinter as tk
from controller import CalculatorController


class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator - Improved Version")
        self.root.geometry("360x570")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")  # açık arka plan

        self.display_var = tk.StringVar(value="0")

        self.create_display()
        self.create_buttons()

        self.controller = CalculatorController(self)

        # Keyboard bindings
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Return>", lambda event: self.controller.handle_input("="))
        self.root.bind("<BackSpace>", lambda event: self.controller.handle_input("⌫"))
        self.root.bind("<Escape>", lambda event: self.controller.handle_input("C"))

    # -----------------------------
    # DISPLAY
    # -----------------------------
    def create_display(self):
        display_frame = tk.Frame(self.root, bg="#f5f5f5")
        display_frame.pack(fill="x", padx=10, pady=10)

        display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 30, "bold"),
            bg="white",
            fg="black",
            anchor="e",
            relief="ridge",
            bd=5,
            height=2
        )
        display_label.pack(fill="both")

    # -----------------------------
    # BUTTONS
    # -----------------------------
    def create_buttons(self):
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        buttons = [
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "x"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", "="]
        ]

        for r, row in enumerate(buttons):
            frame.rowconfigure(r, weight=1)
            for c, text in enumerate(row):
                frame.columnconfigure(c, weight=1)

                if r == 4 and c == 2:
                    continue

                button = tk.Button(
                    frame,
                    text=text,
                    font=("Arial", 18, "bold"),
                    bd=1,
                    relief="solid",
                    fg="black",
                    bg=self.get_button_color(text),
                    activebackground="#dcdcdc",
                    command=lambda t=text: self.controller.handle_input(t)
                )

                # "=" geniş buton
                if r == 4 and c == 3:
                    button.grid(row=r, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)
                else:
                    button.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)

    # -----------------------------
    # BUTTON COLORS
    # -----------------------------
    def get_button_color(self, text):
        if text in ["+", "-", "x", "/"]:
            return "#ffcc80"  # açık turuncu
        elif text == "=":
            return "#81c784"  # açık yeşil
        elif text in ["C", "⌫", "%"]:
            return "#e0e0e0"  # gri
        else:
            return "#fafafa"  # beyaz

    # -----------------------------
    # DISPLAY UPDATE
    # -----------------------------
    def set_display(self, value: str):
        self.display_var.set(value)

    # -----------------------------
    # KEYBOARD INPUT
    # -----------------------------
    def on_key_press(self, event):
        if event.char:
            self.controller.handle_keyboard(event.char)