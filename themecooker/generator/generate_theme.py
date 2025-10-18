#!/usr/bin/env python3
"""Generate full theme (config + all assets) only from a theme name."""

from __future__ import annotations
import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence
import yaml
from jinja2 import Template
import os
import sys

# ────────────────────────────────────────────────
#  Configuración base
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATES_DIR = BASE_DIR / "templates"

@dataclass(frozen=True)
class TemplateSpec:
    name: str
    template_filename: str
    output_filename: str
    config_key: str

TEMPLATED_COMPONENTS: List[TemplateSpec] = [
    TemplateSpec("alacritty", "alacritty_template.toml", "alacritty.toml", "alacritty"),
    TemplateSpec("btop", "btop_template.theme", "btop.theme", "btop"),
    TemplateSpec("chromium", "chromium_template.theme", "chromium.theme", "chromium"),
    TemplateSpec("eza", "eza_template.yml", "eza.yml", "eza"),
    TemplateSpec("hyprland", "hyprland_template.conf", "hyprland.conf", "hyprland"),
    TemplateSpec("hyprlock", "hyprlock_template.conf", "hyprlock.conf", "hyprlock"),
    TemplateSpec("kitty", "kitty_template.conf", "kitty.conf", "kitty"),
    TemplateSpec("mako", "mako_template.ini", "mako.ini", "mako"),
    TemplateSpec("swayosd", "swayosd_template.css", "swayosd.css", "swayosd"),
    TemplateSpec("walker", "walker_template.css", "walker.css", "walker"),
    TemplateSpec("waybar", "waybar_template.css", "waybar.css", "waybar"),
]

# ────────────────────────────────────────────────
#  Utilidades
# ────────────────────────────────────────────────
def generate_file_from_template(template: Path, data: dict, output: Path):
    text = template.read_text()
    rendered = Template(text).render(data)
    output.write_text(rendered)

def normalize_theme_name(name: str):
    display_name = " ".join(word.capitalize() for word in re.split(r"[-_\s]+", name))
    kebab_name = re.sub(r"[\s_]+", "-", name.lower())
    flat_name = re.sub(r"[-_\s]+", "", name.lower())
    return display_name, kebab_name, flat_name

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

def copy_backgrounds(images_dir: Path, dest_dir: Path):
    if not images_dir.exists() or not images_dir.is_dir():
        print("⚠️  No se encontró carpeta 'images/', omitiendo fondos.")
        return
    backgrounds_dir = dest_dir / "backgrounds"
    backgrounds_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for file in images_dir.iterdir():
        if file.is_file():
            shutil.copy(file, backgrounds_dir / file.name)
            copied += 1
    print(f"🖼️  Copiados {copied} fondos → {backgrounds_dir}")

# ────────────────────────────────────────────────
#  Generadores simples
# ────────────────────────────────────────────────
def gen_icons(theme: str) -> str:
    return f"{theme}\n"

def gen_ghostty(theme: str) -> str:
    return f"theme = {theme}\n"

def gen_neovim(theme: str) -> str:
    return f"""return {{
    {{
        "LazyVim/LazyVim",
        opts = {{ colorscheme = "{theme}" }},
    }},
}}"""

def gen_vscode(theme: str) -> str:
    display, kebab, flat = normalize_theme_name(theme)
    return json.dumps({"name": display, "extension": f"{flat}.{kebab}"}, indent=2)

SIMPLE_COMPONENTS: Dict[str, Callable[[str], str]] = {
    "icons": gen_icons,
    "ghostty": gen_ghostty,
    "neovim": gen_neovim,
    "vscode": gen_vscode,
}

# ────────────────────────────────────────────────
#  Generar config a partir de nombre
# ────────────────────────────────────────────────
def generate_theme_config(theme_name: str) -> Path:
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

    print(f"✅ Generated resolved config → {output_path.resolve()}")
    return output_path

# ────────────────────────────────────────────────
#  Generar todos los assets
# ────────────────────────────────────────────────
def build_theme_from_config(config_path: Path):
    theme_name = config_path.stem.replace("_configuration", "")
    templates_dir = DEFAULT_TEMPLATES_DIR
    output_dir = Path.cwd() / theme_name
    images_dir = Path.cwd() / "images"

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✨ Generando theme '{theme_name}' desde {config_path.name}")
    print(f"📦 Carpeta de salida → {output_dir}")

    config = load_yaml(config_path)

    # Plantillas
    for spec in TEMPLATED_COMPONENTS:
        template_path = templates_dir / spec.template_filename
        data = config.get(spec.config_key, {})
        out_path = output_dir / spec.output_filename
        generate_file_from_template(template_path, data, out_path)
        print(f"  • {spec.name}: {out_path.name}")

    # Archivos simples
    for name, generator in SIMPLE_COMPONENTS.items():
        out_file = output_dir / {
            "icons": "icons.theme",
            "ghostty": "ghostty.conf",
            "neovim": "neovim.lua",
            "vscode": "vscode.json",
        }[name]
        out_file.write_text(generator(theme_name))
        print(f"  • {name}: {out_file.name}")

    copy_backgrounds(images_dir, output_dir)
    print(f"✅ Theme '{theme_name}' generado correctamente en {output_dir}")

# ────────────────────────────────────────────────
#  CLI principal
# ────────────────────────────────────────────────
def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate full theme from a theme name.")
    parser.add_argument("theme_name", help="Nombre del theme (ej. embention)")
    args = parser.parse_args(argv)
    theme_name = args.theme_name

    config_path = generate_theme_config(theme_name)
    build_theme_from_config(config_path)
    return 0

if __name__ == "__main__":
    sys.exit(main())
