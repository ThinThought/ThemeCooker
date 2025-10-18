#!/usr/bin/env python3
"""Generate a configuration.yaml with resolved hex colors from extracted_colors.yaml."""
import os
from pathlib import Path
import sys
import yaml


def load_yaml(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"❌ File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def resolve_colors(node, color_map):
    """Recursively replace color_XX keys with hex values."""
    if isinstance(node, dict):
        return {k: resolve_colors(v, color_map) for k, v in node.items()}
    elif isinstance(node, list):
        return [resolve_colors(v, color_map) for v in node]
    elif isinstance(node, str) and node.startswith("color_"):
        return color_map.get(node, node)
    else:
        return node


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_theme_config.py <theme_name>")
        sys.exit(1)

    theme_name = sys.argv[1]
    cwd = Path.cwd()

    colors_path = cwd / "colors_extracted.yaml"
    template_path = cwd / "template_configuration.yaml"
    output_path = cwd / f"{theme_name}_configuration.yaml"

    print(f"🎨 Using extracted colors → {colors_path}")
    print(f"🧩 Using template config → {template_path}")

    colors_data = load_yaml(colors_path)
    config_template = load_yaml(template_path)

    resolved_config = resolve_colors(config_template, colors_data)

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(resolved_config, f, sort_keys=False, allow_unicode=True)
    os.system(f"rm {template_path}")
    os.system(f"rm {colors_path}")

    print(f"✅ Generated resolved config → {output_path.resolve()}")


if __name__ == "__main__":
    main()
