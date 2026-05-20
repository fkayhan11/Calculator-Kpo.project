import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from utils import APP_NAME
from app_paths import user_config_path


@dataclass(frozen=True)
class _ConfigDefaults:
    window_width: int = 420
    window_height: int = 700
    font_family: str = "TkDefaultFont"
    font_size: int = 18
    cursor: str = "hand2"
    theme: str = "Modern Dark"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "window_width": self.window_width,
            "window_height": self.window_height,
            "font_family": self.font_family,
            "font_size": self.font_size,
            "cursor": self.cursor,
            "theme": self.theme,
        }


class ConfigManager:
    """
    Robust JSON config helper:
    - Auto-creates missing config file
    - Safely merges defaults with user config
    - Atomic saves (tmp + replace)
    - Keeps compatibility with existing relative config.json usage
    """

    def __init__(self, filename: str = "config.json"):
        self._defaults = _ConfigDefaults()
        self.path = self._resolve_path(filename)
        self.config: Dict[str, Any] = self.load_config()

    def _resolve_path(self, filename: str) -> Path:
        candidate = Path(filename)
        if candidate.is_absolute():
            return candidate

        # Compatibility: prefer an existing config in the current working directory.
        cwd_path = Path.cwd() / filename
        if cwd_path.exists():
            return cwd_path

        # Stable default: store config in the user profile (works for .app bundles too).
        return user_config_path(APP_NAME, filename)

    def load_config(self):
        defaults = self._defaults.as_dict()

        try:
            if not self.path.exists():
                self.save_config(defaults)
                return dict(defaults)

            with self.path.open("r", encoding="utf-8") as file:
                loaded = json.load(file)

            if not isinstance(loaded, dict):
                raise json.JSONDecodeError("Root is not an object", doc="", pos=0)

            merged = dict(defaults)
            merged.update(loaded)
            return merged

        except json.JSONDecodeError:
            # Preserve corrupt config for debugging; continue with defaults.
            try:
                corrupt_path = self.path.with_suffix(self.path.suffix + ".corrupt")
                if self.path.exists() and not corrupt_path.exists():
                    self.path.replace(corrupt_path)
            except Exception:
                pass

            self.save_config(defaults)
            return dict(defaults)

    def save_config(self, config_data=None):
        if config_data is None:
            config_data = self.config

        # Ensure destination directory exists.
        self.path.parent.mkdir(parents=True, exist_ok=True)

        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as file:
            json.dump(config_data, file, indent=4, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())

        tmp_path.replace(self.path)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def update(self, values: Dict[str, Any]) -> None:
        self.config.update(values)
        self.save_config()

    def ensure(self, key: str, value: Any) -> Any:
        if key not in self.config:
            self.config[key] = value
            self.save_config()
        return self.config[key]
