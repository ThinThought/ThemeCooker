#!/usr/bin/env python3
"""Analyze a configuration.yaml and extract its color palette."""

import re
import os
import sys
from typing import Any, Dict, Set
from pathlib import Path
from PIL import Image, ImageDraw
import yaml

# ─────────────────────────────────────────────────────────────
# Config
GRID_COLS = 5
GRID_ROWS = 7
IMG_WIDTH, IMG_HEIGHT = 500, 750
CELL_W = IMG_WIDTH // GRID_COLS
CELL_H = IMG_HEIGHT // GRID_ROWS

COLOR_PATTERN = re.compile(r"^#?(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6,8})$")

# ─────────────────────────────────────────────────────────────
def normalize_hex(value: str) -> str:
    """Ensure color is a valid hex (#RRGGBB)."""
    value = str(value).strip()
    if not value.startswith("#"):
        value = "#" + value
    return value


def generate_palette_preview_png(colors_dict: Dict[str, str], out_path: Path) -> None:
    """Generate PNG preview (5x7 grid) from colors.yaml dict."""
    colors = [v for k, v in sorted(colors_dict.items(), key=lambda x: int(x[0].split("_")[1]))]
    colors = [normalize_hex(c) for c in colors]

    img = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    for idx, color in enumerate(colors[:GRID_COLS * GRID_ROWS]):
        row, col = divmod(idx, GRID_COLS)
        x0, y0 = col * CELL_W, row * CELL_H
        x1, y1 = x0 + CELL_W, y0 + CELL_H
        draw.rectangle([x0, y0, x1, y1], fill=color, outline="black")

    img.save(out_path)
    print(f"🖼️ Generated → {out_path.resolve()}")


def is_color_value(value: Any) -> bool:
    """Return True when the given scalar looks like a hex color."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    return bool(COLOR_PATTERN.match(stripped))


def collect_colors(node: Any, acc: Set[str]) -> None:
    """Collect unique color strings from YAML data."""
    if isinstance(node, dict):
        for value in node.values():
            collect_colors(value, acc)
    elif isinstance(node, list):
        for item in node:
            collect_colors(item, acc)
    elif is_color_value(node):
        acc.add(node.strip())


def map_config_colors(node: Any, color_lookup: Dict[str, str]) -> Any:
    """Replace color scalars in config with palette keys."""
    if isinstance(node, dict):
        return {k: map_config_colors(v, color_lookup) for k, v in node.items()}
    if isinstance(node, list):
        return [map_config_colors(i, color_lookup) for i in node]
    if isinstance(node, str):
        stripped = node.strip()
        if stripped in color_lookup:
            return color_lookup[stripped]
    return node


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 theme_analyze.py <config.yaml>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)

    data = yaml.safe_load(path.read_text()) or {}

    # Collect palette
    colors: Set[str] = set()
    collect_colors(data, colors)
    sorted_colors = sorted(colors)
    color_dict = {f"color_{i}": normalize_hex(c) for i, c in enumerate(sorted_colors)}

    # Map config to palette keys
    color_lookup = {v: k for k, v in color_dict.items()}
    mapped_config = map_config_colors(data, color_lookup)

    # Always save in current working directory
    cwd = Path(os.getcwd())
    out_png = cwd / "palette_preview.png"
    generate_palette_preview_png(color_dict, out_png)

    print(f"\n📄 File analyzed: {path.name}")
    print(f"🎨 Unique colors: {len(color_dict)}")
    print("✅ Outputs saved:")
    print(f"   - {out_png.name}")


if __name__ == "__main__":
    main()
