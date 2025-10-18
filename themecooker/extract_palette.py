#!/usr/bin/env python3
"""Extract dominant colors from ./images and export colors.yaml"""

from pathlib import Path
from PIL import Image
import yaml
from collections import Counter

MAX_COLORS = 37
COLOR_DEPTH = 8  # reduce palette to 8 bits/channel for speed


def extract_colors_from_image(image_path: Path, max_colors=10):
    """Return most common colors (as hex) from an image."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((100, 100))  # speed up
    img = img.quantize(colors=max_colors)
    palette = img.getpalette()
    color_counts = sorted(img.getcolors(), reverse=True)
    colors = []
    for count, color_index in color_counts:
        r, g, b = palette[color_index * 3: color_index * 3 + 3]
        colors.append(f"#{r:02x}{g:02x}{b:02x}")
    return colors


def main():
    backgrounds_dir = Path.cwd() / "images"
    if not backgrounds_dir.exists():
        print(f"❌ No images directory found at {backgrounds_dir}")
        return

    all_colors = []
    for img_path in backgrounds_dir.glob("*"):
        if img_path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
            continue
        print(f"🎨 Processing {img_path.name}")
        all_colors.extend(extract_colors_from_image(img_path, max_colors=10))

    # Count and select most frequent
    counter = Counter(all_colors)
    most_common = [color for color, _ in counter.most_common(MAX_COLORS)]

    # Build dict color_0 ... color_n
    color_dict = {f"color_{i}": c for i, c in enumerate(most_common)}

    output_path = Path.cwd() / "colors_extracted.yaml"
    with open(output_path, "w") as f:
        yaml.safe_dump(color_dict, f, sort_keys=True, allow_unicode=True)

    print(f"✅ Extracted {len(color_dict)} colors → {output_path.resolve()}")


if __name__ == "__main__":
    main()
