import tkinter as tk
import sys
from pathlib import Path
import traceback
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from view import CalculatorView
from welcome_screen import WelcomeScreen
from config_manager import ConfigManager
from app_paths import user_data_dir
from utils import APP_NAME


config_manager = ConfigManager()

def _write_crash_log(exc: BaseException) -> None:
    try:
        log_path = user_data_dir(APP_NAME) / "crash.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        payload = (
            f"Time: {datetime.now().isoformat(timespec='seconds')}\n"
            f"Python: {sys.version}\n"
            f"Exception: {type(exc).__name__}: {exc}\n\n"
            f"{traceback.format_exc()}\n"
        )
        log_path.write_text(payload, encoding="utf-8")
        print(f"[Calculator] Crash details written to: {log_path}")
    except Exception:
        pass


try:
    root = tk.Tk()
except Exception as exc:
    _write_crash_log(exc)
    raise

# Bring the window to front (helps when users think it "didn't open").
try:
    root.after(50, lambda: root.lift())
    root.after(60, lambda: root.focus_force())
except Exception:
    pass

# If something fails after Tk is available, show a user-friendly dialog as well.
def _show_startup_error(exc: BaseException) -> None:
    try:
        from tkinter import messagebox

        messagebox.showerror(
            "Startup Error",
            "Calculator failed to start.\n\n"
            f"Details: {type(exc).__name__}: {exc}\n\n"
            f"A log file was written to:\n{user_data_dir(APP_NAME) / 'crash.log'}",
        )
    except Exception:
        pass


def start_calculator(theme_name: str):
    # Switch screens inside the same Tk instance for stability.
    if hasattr(root, "_welcome_screen"):
        try:
            root._welcome_screen.destroy()
        except Exception:
            pass

    try:
        app = CalculatorView(root)
        root._calculator_view = app  # keep a strong reference for Tk callbacks
        app.apply_theme(theme_name)
    except Exception as exc:
        _write_crash_log(exc)
        _show_startup_error(exc)
        raise


try:
    root._welcome_screen = WelcomeScreen(
        root,
        start_calculator,
        config_manager,
    )
except Exception as exc:
    _write_crash_log(exc)
    _show_startup_error(exc)
    raise

root.mainloop()
