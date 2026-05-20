import tkinter as tk
from tkinter import messagebox
from typing import Any, Dict, Optional

from history_manager import HistoryManager
from app_paths import user_data_dir
from utils import APP_NAME


class HistoryWindow:
    def __init__(
        self,
        parent: tk.Tk,
        history_manager: HistoryManager,
        theme: Optional[Dict[str, Any]] = None,
    ):
        self.parent = parent
        self.history_manager = history_manager
        self.theme: Dict[str, Any] = theme or {}

        self.window = tk.Toplevel(parent)
        self.window.title("Calculator History")
        self.window.geometry("600x460")
        self.window.minsize(520, 360)
        self.window.transient(parent)

        try:
            self.window.grab_set()
        except Exception:
            pass

        self.root_frame = tk.Frame(self.window, bd=0)
        self.root_frame.pack(fill="both", expand=True, padx=14, pady=14)

        header = tk.Frame(self.root_frame, bd=0)
        header.pack(fill="x")
        self.title_label = tk.Label(header, text="History", font=("Arial", 16, "bold"))
        self.title_label.pack(side="left", anchor="w")

        self.count_label = tk.Label(header, text="", font=("Arial", 10))
        self.count_label.pack(side="right", anchor="e")

        body = tk.Frame(self.root_frame, bd=0)
        body.pack(fill="both", expand=True, pady=(12, 12))

        self.text = tk.Text(body, wrap="word", font=("Consolas", 11), bd=0, padx=10, pady=10)
        self.scroll = tk.Scrollbar(body, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)

        self.text.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

        footer = tk.Frame(self.root_frame, bd=0)
        footer.pack(fill="x")

        self.clear_btn = tk.Button(footer, text="Clear", width=12, command=self.clear)
        self.txt_btn = tk.Button(footer, text="Export TXT", width=12, command=self.export_txt)
        self.csv_btn = tk.Button(footer, text="Export CSV", width=12, command=self.export_csv)
        self.close_btn = tk.Button(footer, text="Close", width=12, command=self.window.destroy)

        self.clear_btn.pack(side="left")
        self.txt_btn.pack(side="left", padx=(10, 0))
        self.csv_btn.pack(side="left", padx=(10, 0))
        self.close_btn.pack(side="right")

        self.apply_theme(self.theme)
        self.refresh()

    def focus(self) -> None:
        try:
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
        except Exception:
            pass

    def refresh(self) -> None:
        lines = self.history_manager.read_history()
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        if lines:
            self.text.insert(tk.END, "".join(lines))
            self.count_label.configure(text=f"{len(lines)} entries")
        else:
            self.text.insert(tk.END, "No history yet.")
            self.count_label.configure(text="0 entries")
        self.text.configure(state="disabled")

    def clear(self) -> None:
        if not messagebox.askyesno("Clear History", "Clear all saved history?"):
            return
        self.history_manager.clear_history()
        self.refresh()

    def export_txt(self) -> None:
        self.history_manager.export_txt()
        from pathlib import Path
        path = user_data_dir(APP_NAME) / "exports/history_export.txt"
        messagebox.showinfo("Export", f"Exported to {path}")

    def export_csv(self) -> None:
        self.history_manager.export_csv()
        from pathlib import Path
        path = user_data_dir(APP_NAME) / "exports/history_export.csv"
        messagebox.showinfo("Export", f"Exported to {path}")

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        self.theme = theme or {}
        bg = self.theme.get("bg", "#f5f5f5")
        panel = self.theme.get("panel_bg", bg)
        fg = self.theme.get("panel_fg", self.theme.get("fg", "black"))
        border = self.theme.get("border", "#d0d0d0")
        display_bg = self.theme.get("display_bg", "#ffffff")
        display_fg = self.theme.get("display_fg", fg)

        self.window.configure(bg=bg)
        self.root_frame.configure(bg=panel, highlightthickness=1, highlightbackground=border)

        for w in [self.title_label, self.count_label]:
            w.configure(bg=panel, fg=fg)

        self.text.configure(
            bg=display_bg,
            fg=display_fg,
            insertbackground=display_fg,
            selectbackground=self.theme.get("accent", "#2b7cff"),
            selectforeground=self.theme.get("menu_active_fg", "#ffffff"),
        )

        # Buttons
        btn_bg = self.theme.get("button_fn_bg", self.theme.get("button_bg", "#eaeaea"))
        btn_fg = self.theme.get("button_fn_fg", self.theme.get("button_fg", fg))
        hover = self.theme.get("button_hover_bg", "#cce7ff")
        active_bg = self.theme.get("button_active_bg", "#dcdcdc")

        for b in [self.clear_btn, self.txt_btn, self.csv_btn, self.close_btn]:
            b.configure(
                bg=btn_bg,
                fg=btn_fg,
                bd=0,
                activebackground=active_bg,
                activeforeground=btn_fg,
                cursor="hand2",
                padx=10,
                pady=8,
            )
            b.bind("<Enter>", lambda e, bb=b: bb.configure(bg=hover))
            b.bind("<Leave>", lambda e, bb=b: bb.configure(bg=btn_bg))
