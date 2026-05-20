#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "PyInstaller is not installed in the current environment."
  echo "Install it first: pip install pyinstaller"
  exit 1
fi

if [[ -f "resources/icon.png" && ! -f "resources/icon.icns" ]]; then
  echo "Generating resources/icon.icns from resources/icon.png ..."
  bash packaging/macos/make_icns.sh
fi

ICON_ARG=()
if [[ -f "resources/icon.icns" ]]; then
  ICON_ARG=(--icon "resources/icon.icns")
fi

pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "Advanced Calculator" \
  "${ICON_ARG[@]}" \
  --add-data "resources/about.jpg:resources" \
  --add-data "resources/icon.jpg:resources" \
  --add-data "resources/icon.png:resources" \
  main.py

echo "Build complete."
echo "App bundle: dist/Advanced Calculator.app"

