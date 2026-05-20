import tkinter as tk
from typing import Any, Dict, Optional


class ButtonFactory:
    """
    Factory class for creating calculator buttons.
    """

    @staticmethod
    def create_button(
        parent,
        text,
        command,
        cursor="hand2",
        font_family="Arial",
        font_size=18,
        theme: Optional[Dict[str, Any]] = None
    ):

        theme = theme or {}
        bg = ButtonFactory.get_button_color(text, theme=theme)
        fg = ButtonFactory.get_button_fg(text, theme=theme)
        active_bg = theme.get("button_active_bg", "#dcdcdc")
        border = theme.get("border", "#d0d0d0")

        button = tk.Button(
            parent,
            text=text,
            font=(font_family, font_size, "bold"),
            bd=0,
            relief="flat",
            fg=fg,
            bg=bg,
            activebackground=active_bg,
            activeforeground=fg,
            highlightthickness=1,
            highlightbackground=border,
            highlightcolor=border,
            cursor=cursor,
            command=command
        )

        return button

    @staticmethod
    def _button_kind(text: str) -> str:
        if text in ["+", "-", "x", "/"]:
            return "op"
        if text == "=":
            return "eq"
        if text in ["C", "⌫", "%", "√", "x²", "±"]:
            return "fn"
        if text in ["MC", "MR", "M+", "M-"]:
            return "mem"
        return "num"

    @staticmethod
    def get_button_color(text: str, theme: Optional[Dict[str, Any]] = None) -> str:
        theme = theme or {}
        kind = ButtonFactory._button_kind(text)
        return theme.get(f"button_{kind}_bg", theme.get("button_bg", "#fafafa"))

    @staticmethod
    def get_button_fg(text: str, theme: Optional[Dict[str, Any]] = None) -> str:
        theme = theme or {}
        kind = ButtonFactory._button_kind(text)
        return theme.get(f"button_{kind}_fg", theme.get("button_fg", "black"))
