import tkinter as tk
from tkinter import Menu, Toplevel, Label
from PIL import Image, ImageTk


from controller import CalculatorController
from button_factory import ButtonFactory


class CalculatorView:
    def __init__(self, root):
        self.root = root

        self.root.title("Calculator - Improved Version")
        self.root.geometry("360x570")
        self.root.resizable(False, False)

        # Theme
        self.dark_mode = False
        self.bg_color = "#f5f5f5"
        self.fg_color = "black"

        self.root.configure(bg=self.bg_color)

        # Cursor
        self.root.config(cursor="hand2")

        # Icon
        try:
            icon = Image.open("resources/icon.jpg")
            icon = icon.resize((32, 32))

            self.icon_image = ImageTk.PhotoImage(icon)
            self.root.iconphoto(True, self.icon_image)

        except Exception:
            print("Icon could not be loaded.")

        self.display_var = tk.StringVar(value="0")

        self.create_display()
        self.create_menu()
        self.create_buttons()

        self.controller = CalculatorController(self)

        # Keyboard bindings
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind(
            "<Return>",
            lambda event: self.controller.handle_input("=")
        )

        self.root.bind(
            "<BackSpace>",
            lambda event: self.controller.handle_input("⌫")
        )

        self.root.bind(
            "<Escape>",
            lambda event: self.controller.handle_input("C")
        )

    def create_display(self):
        display_frame = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        display_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 30, "bold"),
            bg="white",
            fg=self.fg_color,
            anchor="e",
            relief="ridge",
            bd=5,
            height=2
        )

        self.display_label.pack(fill="both")

    def create_buttons(self):
        self.button_frame = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        self.button_frame.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        buttons = [
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "x"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", "="]
        ]

        for r, row in enumerate(buttons):
            self.button_frame.rowconfigure(r, weight=1)

            for c, text in enumerate(row):
                self.button_frame.columnconfigure(c, weight=1)

                if r == 4 and c == 2:
                    continue

                button = ButtonFactory.create_button(
                    parent=self.button_frame,
                    text=text,
                    command=lambda t=text: self.button_click(t)
                )

                if r == 4 and c == 3:
                    button.grid(
                        row=r,
                        column=2,
                        columnspan=2,
                        sticky="nsew",
                        padx=5,
                        pady=5
                    )
                else:
                    button.grid(
                        row=r,
                        column=c,
                        sticky="nsew",
                        padx=5,
                        pady=5
                    )

    def create_menu(self):
        menu_bar = Menu(self.root)

        # File menu
        file_menu = Menu(menu_bar, tearoff=0)

        file_menu.add_command(
            label="Exit",
            command=self.root.quit
        )

        # View menu
        view_menu = Menu(menu_bar, tearoff=0)

        view_menu.add_command(
            label="Toggle Dark Mode",
            command=self.toggle_theme
        )

        # Help menu
        help_menu = Menu(menu_bar, tearoff=0)

        help_menu.add_command(
            label="About",
            command=self.show_about
        )

        menu_bar.add_cascade(
            label="File",
            menu=file_menu
        )

        menu_bar.add_cascade(
            label="View",
            menu=view_menu
        )

        menu_bar.add_cascade(
            label="Help",
            menu=help_menu
        )

        self.root.config(menu=menu_bar)

    def show_about(self):
        about_window = Toplevel(self.root)

        about_window.title("About")
        about_window.geometry("320x320")
        about_window.resizable(False, False)

        try:
            image = Image.open("resources/about.jpg")
            image = image.resize((120, 120))

            photo = ImageTk.PhotoImage(image)

            image_label = Label(
                about_window,
                image=photo
            )

            image_label.image = photo
            image_label.pack(pady=10)

        except Exception:
            print("About image could not be loaded.")

        text = Label(
            about_window,
            text=(
                "Calculator Project\n"
                "Lab 6 - Application Resources\n\n"
                "Developer: Furkan\n"
                "Technology: Python Tkinter\n"
                "Architecture: MVC\n"
                "Patterns: Factory / Command / Decorator"
            ),
            font=("Arial", 11)
        )

        text.pack(pady=10)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.bg_color = "#2b2b2b"
            self.fg_color = "white"

            self.display_label.configure(
                bg="#1e1e1e",
                fg="white"
            )

        else:
            self.bg_color = "#f5f5f5"
            self.fg_color = "black"

            self.display_label.configure(
                bg="white",
                fg="black"
            )

        self.root.configure(bg=self.bg_color)
        self.button_frame.configure(bg=self.bg_color)

    def button_click(self, value):


        self.controller.handle_input(value)

    def set_display(self, value: str):
        self.display_var.set(value)

    def on_key_press(self, event):
        if event.char:
            self.controller.handle_keyboard(event.char)