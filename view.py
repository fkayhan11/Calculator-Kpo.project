from utils import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_MONO_FONT_CANDIDATES,
    DEFAULT_UI_FONT_CANDIDATES,
    THEMES,
)
from ui_components import UIComponents
import tkinter as tk
from tkinter import Menu, Label
import tkinter.font as tkfont
from pathlib import Path
try:
    from PIL import Image, ImageTk
except Exception:  # Pillow missing or broken; run without images
    Image = None
    ImageTk = None

from controller import CalculatorController
from button_factory import ButtonFactory
from config_manager import ConfigManager
from history_manager import HistoryManager
from history_window import HistoryWindow
from typing import Optional, List
from app_paths import resource_path


class CalculatorView:

    def __init__(self, root):

        self.root = root
        self._base_dir = Path(__file__).resolve().parent

        # Config
        self.config_manager = ConfigManager()

        # History
        self.history_manager = HistoryManager()
        self._history_window: Optional[HistoryWindow] = None
        self._about_window = None

        # Window size
        width = self.config_manager.get(
            "window_width",
            420
        )

        height = self.config_manager.get(
            "window_height",
            700
        )

        self.root.title(APP_NAME)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        # Fonts (make text readable even if config font is missing/ugly)
        self.ui_font_size = int(self.config_manager.get("font_size", 18))
        self.ui_font_family = self._resolve_font_family(
            self.config_manager.get("font_family", "TkDefaultFont"),
            DEFAULT_UI_FONT_CANDIDATES,
        )
        self.display_font_family = self._resolve_font_family(
            self.config_manager.get("display_font_family", ""),
            DEFAULT_MONO_FONT_CANDIDATES,
        )
        self.display_font_size = int(self.config_manager.get("display_font_size", 32))

        # Theme (initialized before UI creation)
        self.current_theme_name = self.config_manager.get("theme", "Modern Dark")
        self.current_theme = THEMES.get(self.current_theme_name, THEMES["Modern Dark"])
        self.bg_color = self.current_theme.get("bg", "#f5f5f5")
        self.fg_color = self.current_theme.get("fg", "black")

        self.root.configure(bg=self.bg_color)

        # Cursor
        self.cursor_style = self.config_manager.get(
            "cursor",
            "hand2"
        )

        self.root.config(
            cursor=self.cursor_style
        )

        # Icon
        try:
            if Image is None or ImageTk is None:
                raise RuntimeError("Pillow is not available")

            icon = Image.open(
                resource_path("resources", "icon.jpg")
            )

            icon = icon.resize((32, 32))

            self.icon_image = ImageTk.PhotoImage(
                icon
            )

            self.root.iconphoto(
                True,
                self.icon_image
            )

        except Exception:

            print(
                "Icon could not be loaded."
            )

        # Display variable
        self.display_var = tk.StringVar(
            value="0"
        )
        self._operation_count = 0

        # Create UI
        self.create_display()
        self.create_menu()
        self.create_buttons()
        self.create_status_bar()

        # Controller
        self.controller = CalculatorController(
            self
        )

        # Keyboard bindings
        self.root.bind(
            "<Key>",
            self.on_key_press
        )

        self.root.bind(
            "<Return>",
            lambda event:
            self.controller.handle_input("=")
        )

        self.root.bind(
            "<BackSpace>",
            lambda event:
            self.controller.handle_input("⌫")
        )

        self.root.bind(
            "<Escape>",
            lambda event:
            self.controller.handle_input("C")
        )

        # Apply saved theme
        saved_theme = self.config_manager.get(
            "theme",
            "Classic"
        )

        self.apply_theme(saved_theme)

    def _resolve_font_family(self, requested: str, fallbacks: List[str]) -> str:
        requested = (requested or "").strip()
        try:
            families = set(tkfont.families(self.root))
        except Exception:
            families = set()

        # Named Tk fonts are always safe.
        if requested in {"TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont", "TkFixedFont"}:
            return requested

        if requested and requested in families:
            return requested

        for candidate in fallbacks:
            if candidate in families:
                return candidate

        return "TkDefaultFont"

    def create_display(self):

        self.display_frame = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        self.display_frame.pack(
            fill="x",
            padx=14,
            pady=(14, 10)
        )

        self.display_label = UIComponents.create_display(
            parent=self.display_frame,
            textvariable=self.display_var,
            font_family=self.display_font_family,
            font_size=self.display_font_size,
            bg=self.current_theme.get("display_bg", "white"),
            fg=self.current_theme.get("display_fg", self.fg_color),
            border_color=self.current_theme.get("border", "#d0d0d0"),
            font_weight="normal"
        )

        self.display_label.pack(
            fill="both"
        )

    def create_buttons(self):

        self.button_frame = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        self.button_frame.pack(
            expand=True,
            fill="both",
            padx=14,
            pady=(0, 10)
        )

        # Grid spec: entries can be:
        # - "TEXT" (1 cell)
        # - ("TEXT", colspan, rowspan)
        grid = [
            ["MC", "MR", "M+", "M-"],
            ["√", "x²", "±", "/"],
            ["C", "⌫", "%", "x"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", ("=", 1, 2)],
            [("0", 2, 1), None, ".", None],
        ]

        for r, row in enumerate(grid):
            self.button_frame.rowconfigure(r, weight=1)
            for c in range(4):
                self.button_frame.columnconfigure(c, weight=1)

            c = 0
            while c < 4:
                cell = row[c] if c < len(row) else None
                if cell is None:
                    c += 1
                    continue

                if isinstance(cell, tuple):
                    text, colspan, rowspan = cell
                else:
                    text, colspan, rowspan = cell, 1, 1

                button = ButtonFactory.create_button(
                    parent=self.button_frame,
                    text=text,
                    command=lambda t=text: self.button_click(t),
                    cursor=self.cursor_style,
                    font_family=self.ui_font_family,
                    font_size=self.ui_font_size,
                    theme=self.current_theme,
                )

                # Hover effect (theme-aware)
                button.bind(
                    "<Enter>",
                    lambda e, b=button: b.configure(
                        bg=self.current_theme.get("button_hover_bg", "#cce7ff")
                    ),
                )
                button.bind(
                    "<Leave>",
                    lambda e, b=button, t=text: b.configure(
                        bg=ButtonFactory.get_button_color(t, theme=self.current_theme)
                    ),
                )

                button.grid(
                    row=r,
                    column=c,
                    columnspan=colspan,
                    rowspan=rowspan,
                    sticky="nsew",
                    padx=6,
                    pady=6,
                )

                c += colspan

    def create_status_bar(self):

        self.status_bar = tk.Label(
            self.root,
            text=f"{APP_NAME} v{APP_VERSION}",
            bd=1,
            relief=tk.SUNKEN,
            anchor="w",
            font=(self.ui_font_family, 10, "normal")
        )

        self.status_bar.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

    def create_menu(self):

        self.menu_bar = Menu(
            self.root
        )

        # FILE MENU
        file_menu = Menu(
            self.menu_bar,
            tearoff=0
        )

        file_menu.add_command(
            label="Exit",
            command=self.root.quit
        )

        # VIEW MENU
        view_menu = Menu(
            self.menu_bar,
            tearoff=0
        )

        view_menu.add_command(
            label="Toggle Dark Mode",
            command=self.toggle_dark_mode
        )

        # THEMES MENU
        themes_menu = Menu(
            self.menu_bar,
            tearoff=0
        )

        for theme_name in THEMES.keys():

            themes_menu.add_command(
                label=theme_name,
                command=lambda t=theme_name:
                self.apply_theme(t)
            )

        # HISTORY MENU
        history_menu = Menu(
            self.menu_bar,
            tearoff=0
        )

        history_menu.add_command(
            label="Show History",
            command=self.show_history
        )

        history_menu.add_command(
            label="Clear History",
            command=self.clear_history
        )

        history_menu.add_command(
            label="Export TXT",
            command=self.export_history_txt
        )

        history_menu.add_command(
            label="Export CSV",
            command=self.export_history_csv
        )

        # HELP MENU
        help_menu = Menu(
            self.menu_bar,
            tearoff=0
        )

        help_menu.add_command(
            label="About",
            command=self.show_about
        )

        # ADD CASCADES
        self.menu_bar.add_cascade(
            label="File",
            menu=file_menu
        )

        self.menu_bar.add_cascade(
            label="View",
            menu=view_menu
        )

        self.menu_bar.add_cascade(
            label="Themes",
            menu=themes_menu
        )

        self.menu_bar.add_cascade(
            label="History",
            menu=history_menu
        )

        self.menu_bar.add_cascade(
            label="Help",
            menu=help_menu
        )

        self.root.config(
            menu=self.menu_bar
        )

        self._menus = [file_menu, view_menu, themes_menu, history_menu, help_menu]

    def show_about(self):
        if self._about_window is not None:
            try:
                if self._about_window.winfo_exists():
                    self._about_window.lift()
                    self._about_window.focus_force()
                    return
            except Exception:
                pass

        about_window = UIComponents.create_popup(
            title="About",
            geometry="460x480",
            parent=self.root
        )
        self._about_window = about_window

        theme = self.current_theme or {}
        bg = theme.get("bg", "#f5f5f5")
        panel = theme.get("panel_bg", bg)
        fg = theme.get("panel_fg", theme.get("fg", "black"))
        border = theme.get("border", "#d0d0d0")

        about_window.configure(bg=bg)
        wrapper = tk.Frame(about_window, bg=panel, highlightthickness=1, highlightbackground=border)
        wrapper.pack(fill="both", expand=True, padx=14, pady=14)

        try:
            if Image is None or ImageTk is None:
                raise RuntimeError("Pillow is not available")

            image = Image.open(
                resource_path("resources", "about.jpg")
            )

            image = image.resize(
                (120, 120)
            )

            photo = ImageTk.PhotoImage(
                image
            )

            image_label = Label(wrapper, image=photo, bg=panel)

            image_label.image = photo

            image_label.pack(
                pady=(18, 10)
            )

        except Exception:

            print(
                "About image could not be loaded."
            )

        text = Label(
            wrapper,
            text=(
                f"{APP_NAME} v{APP_VERSION}\n\n"
                "Developer: Furkan\n\n"
                "Architecture: MVC\n"
                "Patterns: Factory Method • Decorator • Strategy\n\n"
                "Features:\n"
                "• Theme system with persistence\n"
                "• History window + TXT/CSV export\n"
                "• Hover effects + keyboard support\n"
                "• Advanced GUI layout"
            ),
            font=("Arial", 11),
            justify="left",
            bg=panel,
            fg=fg
        )

        text.pack(
            pady=10,
            padx=18,
            anchor="w"
        )

    def apply_theme(self, theme_name):

        theme = THEMES.get(
            theme_name
        )

        if not theme:
            return

        self.current_theme_name = theme_name
        self.current_theme = theme
        self.bg_color = theme.get("bg", "#f5f5f5")
        self.fg_color = theme.get("fg", "black")

        self.root.configure(
            bg=self.bg_color
        )

        if hasattr(self, "display_frame"):
            self.display_frame.configure(bg=self.bg_color)

        self.button_frame.configure(
            bg=self.bg_color
        )

        self.display_label.configure(
            bg=theme.get("display_bg", "white"),
            fg=theme.get("display_fg", self.fg_color)
        )

        # Update buttons
        for widget in self.button_frame.winfo_children():

            if isinstance(widget, tk.Button):

                widget.configure(
                    fg=ButtonFactory.get_button_fg(widget.cget("text"), theme=theme),
                    bg=ButtonFactory.get_button_color(widget.cget("text"), theme=theme),
                    activebackground=theme.get("button_active_bg", "#dcdcdc"),
                    activeforeground=ButtonFactory.get_button_fg(widget.cget("text"), theme=theme),
                )

        # Save theme
        self.config_manager.set(
            "theme",
            theme_name
        )

        self.status_bar.configure(
            bg=theme.get("status_bg", self.bg_color),
            fg=theme.get("status_fg", self.fg_color),
            text=f"Theme: {theme_name} | v{APP_VERSION} | Ops: {self._operation_count}"
        )

        # Best-effort menu theming (platform dependent).
        try:
            self.menu_bar.configure(
                bg=theme.get("menu_bg", self.bg_color),
                fg=theme.get("menu_fg", self.fg_color),
                activebackground=theme.get("menu_active_bg", theme.get("accent", "#dbe9ff")),
                activeforeground=theme.get("menu_active_fg", self.fg_color),
            )
            for m in getattr(self, "_menus", []):
                m.configure(
                    bg=theme.get("menu_bg", self.bg_color),
                    fg=theme.get("menu_fg", self.fg_color),
                    activebackground=theme.get("menu_active_bg", theme.get("accent", "#dbe9ff")),
                    activeforeground=theme.get("menu_active_fg", self.fg_color),
                )
        except Exception:
            pass

        if self._history_window:
            try:
                if self._history_window.window.winfo_exists():
                    self._history_window.apply_theme(theme)
            except Exception:
                self._history_window = None

        if self._about_window is not None:
            try:
                if self._about_window.winfo_exists():
                    self._about_window.configure(bg=theme.get("bg", self.bg_color))
            except Exception:
                pass

    def toggle_dark_mode(self):

        current = self.config_manager.get(
            "theme",
            "Classic"
        )

        if current != "Modern Dark":

            self.apply_theme(
                "Modern Dark"
            )

        else:

            self.apply_theme(
                "Classic"
            )

    def show_history(self):
        if self._history_window:
            try:
                if self._history_window.window.winfo_exists():
                    self._history_window.apply_theme(self.current_theme)
                    self._history_window.refresh()
                    self._history_window.focus()
                    return
            except Exception:
                self._history_window = None

        self._history_window = HistoryWindow(
            parent=self.root,
            history_manager=self.history_manager,
            theme=self.current_theme,
        )

    def clear_history(self):

        self.history_manager.clear_history()

    def clear_history_window(self, text_area):

        self.history_manager.clear_history()

        text_area.delete(
            "1.0",
            tk.END
        )

        text_area.insert(
            tk.END,
            "History cleared."
        )

    def export_history_txt(self):

        self.history_manager.export_txt()

    def export_history_csv(self):

        self.history_manager.export_csv()

    def button_click(self, value):

        self.controller.handle_input(
            value
        )

    def set_display(self, value: str):

        self.display_var.set(
            value
        )

    def set_operation_count(self, count: int) -> None:
        # Controller calls this after each successful action.
        self._operation_count = int(count)
        theme = self.current_theme or {}
        self.status_bar.configure(
            text=f"Theme: {self.current_theme_name} | v{APP_VERSION} | Ops: {self._operation_count}",
            bg=theme.get("status_bg", self.bg_color),
            fg=theme.get("status_fg", self.fg_color),
        )

    def on_key_press(self, event):

        if event.char:

            self.controller.handle_keyboard(
                event.char
            )
