#!/usr/bin/env python3
"""Generate every supported theme asset from configuration values and templates."""

from __future__ import annotations
import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence
import yaml
from jinja2 import Template

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

def load_configuration(path: Path) -> Dict[str, dict]:
    try:
        data = yaml.safe_load(path.read_text()) or {}
        if not isinstance(data, dict):
            raise TypeError
        return data
    except Exception as e:
        raise SystemExit(f"❌ Error leyendo configuración {path}: {e}")

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
#  CLI principal
# ────────────────────────────────────────────────
def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a complete theme from a configuration YAML.")
    parser.add_argument("config_file", help="Archivo YAML de configuración (ej. tokyonight_configuration.yaml)")
    args = parser.parse_args(argv)

    config_path = Path(args.config_file).expanduser()
    if not config_path.exists():
        raise SystemExit(f"❌ No se encontró el archivo: {config_path}")

    theme_name = config_path.stem.replace("_configuration", "")
    templates_dir = DEFAULT_TEMPLATES_DIR
    output_dir = Path.cwd() / theme_name   # 🔥 genera en el cwd
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"✨ Generando theme '{theme_name}' desde {config_path.name}")
    print(f"📦 Carpeta de salida → {output_dir}")

    config = load_configuration(config_path)

    # Generar con plantillas
    for spec in TEMPLATED_COMPONENTS:
        template_path = templates_dir / spec.template_filename
        data = config.get(spec.config_key, {})
        out_path = output_dir / spec.output_filename
        generate_file_from_template(template_path, data, out_path)
        print(f"  • {spec.name}: {out_path.name}")

    # Generar simples
    for name, generator in SIMPLE_COMPONENTS.items():
        out_file = output_dir / {
            "icons": "icons.theme",
            "ghostty": "ghostty.conf",
            "neovim": "neovim.lua",
            "vscode": "vscode.json",
        }[name]
        out_file.write_text(generator(theme_name))
        print(f"  • {name}: {out_file.name}")

    print(f"✅ Theme '{theme_name}' generado correctamente en {output_dir}")
    return 0

if __name__ == "__main__":
    main()
