import tkinter as tk
from utils import APP_NAME, APP_VERSION, THEMES


class WelcomeScreen:

    def __init__(
            self,
            root,
            start_callback,
            config_manager
    ):

        self.root = root
        self.start_callback = start_callback
        self.config_manager = config_manager

        self.root.title(APP_NAME)
        self.root.geometry("760x560")
        self.root.resizable(False, False)

        saved = self.config_manager.get("theme", "Modern Dark")
        if saved not in THEMES:
            saved = "Modern Dark"

        self.selected_theme = tk.StringVar(value=saved)
        self.selected_theme.trace_add("write", lambda *_: self.apply_preview_theme())

        self.create_ui()
        self.apply_preview_theme()

    def create_ui(self):

        self.container = tk.Frame(
            self.root,
            bg="#1e1e1e"
        )

        self.container.pack(fill="both", expand=True)

        self.card = tk.Frame(self.container, bd=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=620, height=470)

        self.header = tk.Frame(self.card, bd=0)
        self.header.pack(fill="x", padx=28, pady=(26, 12))

        self.title_label = tk.Label(self.header, text=APP_NAME, font=("Arial", 28, "bold"))
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            self.header,
            text="Feature-rich desktop calculator (MVC • Patterns • Themes • History)",
            font=("Arial", 11),
            justify="left",
        )
        self.subtitle_label.pack(anchor="w", pady=(6, 0))

        self.body = tk.Frame(self.card, bd=0)
        self.body.pack(fill="both", expand=True, padx=28, pady=(0, 10))

        self.left = tk.Frame(self.body, bd=0)
        self.right = tk.Frame(self.body, bd=0)
        self.left.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        self.right.grid(row=0, column=1, sticky="nsew")
        self.body.rowconfigure(0, weight=1)
        self.body.columnconfigure(0, weight=1)
        self.body.columnconfigure(1, weight=1)

        self.version_label = tk.Label(self.left, text=f"Version {APP_VERSION}", font=("Arial", 11, "bold"))
        self.version_label.pack(anchor="w", pady=(6, 14))

        self.info_label = tk.Label(
            self.left,
            text=(
                "Highlights:\n"
                "• Multiple design patterns\n"
                "• Theme engine with persistence\n"
                "• History window + TXT/CSV export\n"
                "• Keyboard-friendly controls\n"
                "• Premium UI spacing and typography"
            ),
            font=("Arial", 11),
            justify="left",
        )
        self.info_label.pack(anchor="w")

        self.theme_label = tk.Label(self.right, text="Choose Theme", font=("Arial", 14, "bold"))
        self.theme_label.pack(anchor="w", pady=(6, 10))

        self.themes_frame = tk.Frame(self.right, bd=0)
        self.themes_frame.pack(fill="both", expand=True)

        for theme_name in THEMES.keys():

            button = tk.Radiobutton(
                self.themes_frame,
                text=theme_name,
                variable=self.selected_theme,
                value=theme_name,
                font=("Arial", 11),
                indicatoron=True,
                padx=8,
                pady=2
            )

            button.pack(
                anchor="w"
            )

        self.footer = tk.Frame(self.card, bd=0)
        self.footer.pack(fill="x", padx=28, pady=(0, 22))

        self.start_button = tk.Button(
            self.footer,
            text="Start Calculator",
            font=("Arial", 14, "bold"),
            bd=0,
            cursor=self.config_manager.get("cursor", "hand2"),
            command=self.start_app,
            padx=18,
            pady=10,
        )
        self.start_button.pack(anchor="e")

        self.start_button.bind("<Enter>", lambda e: self._hover(True))
        self.start_button.bind("<Leave>", lambda e: self._hover(False))

    def _hover(self, entering: bool) -> None:
        theme = THEMES.get(self.selected_theme.get(), THEMES["Modern Dark"])
        normal = theme.get("button_eq_bg", theme.get("accent", "#00c853"))
        hover = theme.get("button_hover_bg", normal)
        self.start_button.configure(bg=hover if entering else normal)

    def apply_preview_theme(self) -> None:
        theme = THEMES.get(self.selected_theme.get(), THEMES["Modern Dark"])

        self.container.configure(bg=theme.get("bg", "#1e1e1e"))
        self.card.configure(
            bg=theme.get("panel_bg", theme.get("bg", "#2b2b2b")),
            highlightthickness=1,
            highlightbackground=theme.get("border", "#3a3a3a"),
            highlightcolor=theme.get("border", "#3a3a3a"),
        )

        panel_bg = theme.get("panel_bg", theme.get("bg", "#2b2b2b"))
        for frame in [self.header, self.body, self.left, self.right, self.themes_frame, self.footer]:
            frame.configure(bg=panel_bg)

        for widget in [self.title_label, self.subtitle_label, self.version_label, self.info_label, self.theme_label]:
            widget.configure(
                bg=panel_bg,
                fg=theme.get("panel_fg", theme.get("fg", "white")),
            )

        self.start_button.configure(
            bg=theme.get("button_eq_bg", theme.get("accent", "#00c853")),
            fg=theme.get("button_eq_fg", theme.get("fg", "white")),
            activebackground=theme.get("button_active_bg", theme.get("button_hover_bg", "#00e676")),
            activeforeground=theme.get("button_eq_fg", theme.get("fg", "white")),
        )

        # Theme radio styles
        for rb in self.themes_frame.winfo_children():
            if isinstance(rb, tk.Radiobutton):
                rb.configure(
                    bg=theme.get("panel_bg", theme.get("bg", "#2b2b2b")),
                    fg=theme.get("panel_fg", theme.get("fg", "white")),
                    selectcolor=theme.get("bg", "#1e1e1e"),
                    activebackground=theme.get("panel_bg", theme.get("bg", "#2b2b2b")),
                    activeforeground=theme.get("accent", theme.get("fg", "white")),
                )

    def start_app(self):

        selected = self.selected_theme.get()

        self.config_manager.set(
            "theme",
            selected
        )

        self.start_callback(selected)

    def destroy(self) -> None:
        # Used by main.py to switch screens without destroying the Tk root.
        try:
            self.container.destroy()
        except Exception:
            pass
