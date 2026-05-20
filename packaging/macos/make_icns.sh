#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RES_DIR="$ROOT_DIR/resources"
SRC_PNG="$RES_DIR/icon.png"
OUT_ICNS="$RES_DIR/icon.icns"

if [[ ! -f "$SRC_PNG" ]]; then
  echo "Missing: $SRC_PNG"
  echo "Put a 1024x1024 (or at least 512x512) PNG at resources/icon.png and re-run."
  exit 1
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

ICONSET="$TMP_DIR/icon.iconset"
mkdir -p "$ICONSET"

sizes=(16 32 64 128 256 512 1024)
for s in "${sizes[@]}"; do
  sips -z "$s" "$s" "$SRC_PNG" --out "$ICONSET/icon_${s}x${s}.png" >/dev/null
done

# Retina variants
sips -z 32 32 "$SRC_PNG" --out "$ICONSET/icon_16x16@2x.png" >/dev/null
sips -z 64 64 "$SRC_PNG" --out "$ICONSET/icon_32x32@2x.png" >/dev/null
sips -z 256 256 "$SRC_PNG" --out "$ICONSET/icon_128x128@2x.png" >/dev/null
sips -z 512 512 "$SRC_PNG" --out "$ICONSET/icon_256x256@2x.png" >/dev/null
sips -z 1024 1024 "$SRC_PNG" --out "$ICONSET/icon_512x512@2x.png" >/dev/null

iconutil -c icns "$ICONSET" -o "$OUT_ICNS"
echo "Wrote: $OUT_ICNS"

