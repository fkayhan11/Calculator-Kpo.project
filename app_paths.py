import os
import platform
import sys
from pathlib import Path


def is_frozen() -> bool:
    # PyInstaller sets sys.frozen and sys._MEIPASS.
    return bool(getattr(sys, "frozen", False)) or hasattr(sys, "_MEIPASS")


def resource_base_dir() -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


def resource_path(*parts: str) -> Path:
    return resource_base_dir().joinpath(*parts)


def user_data_dir(app_name: str) -> Path:
    system = platform.system().lower()
    home = Path.home()

    if system == "darwin":
        return home / "Library" / "Application Support" / app_name

    if system == "windows":
        base = os.environ.get("APPDATA") or str(home)
        return Path(base) / app_name

    # Linux / other
    base = os.environ.get("XDG_DATA_HOME") or str(home / ".local" / "share")
    return Path(base) / app_name


def user_config_path(app_name: str, filename: str) -> Path:
    return user_data_dir(app_name) / filename

