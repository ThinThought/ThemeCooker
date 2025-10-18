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
#  Paths y configuración base
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATES_DIR = BASE_DIR / "templates"
DEFAULT_OUTPUT_ROOT = BASE_DIR / "generated"


# ────────────────────────────────────────────────
#  Descripción de cada componente Jinja
# ────────────────────────────────────────────────
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
#  Utilidades comunes
# ────────────────────────────────────────────────
def generate_file_from_template(template: Path | str, data: dict | str, output: Path):
    text = template.read_text() if isinstance(template, Path) else str(template)
    rendered = Template(text).render(data) if isinstance(data, dict) else str(data)
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
#  Generadores simples (sin plantilla)
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


SIMPLE_COMPONENTS: Dict[str, str | Callable[[str], str]] = {
    "icons": gen_icons,
    "ghostty": gen_ghostty,
    "neovim": gen_neovim,
    "vscode": gen_vscode,
}


# ────────────────────────────────────────────────
#  CLI y ejecución principal
# ────────────────────────────────────────────────
def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a complete theme folder from configuration.")
    parser.add_argument("theme_name", help="Nombre del theme (ej. tokyonight)")
    parser.add_argument(
        "--config",
        help="Archivo YAML de configuración (por defecto busca <theme_name>_configuration.yaml o configuration.yaml)",
    )
    parser.add_argument("--templates-dir", default=DEFAULT_TEMPLATES_DIR, help="Directorio de plantillas")
    parser.add_argument("--output-dir", help="Directorio de salida (por defecto ./generated/<theme_name>)")
    parser.add_argument("--only", nargs="+", help="Generar solo componentes indicados")
    args = parser.parse_args(argv)

    theme_name = args.theme_name
    templates_dir = Path(args.templates_dir).expanduser()

    # Auto-detect config path
    if args.config:
        config_path = Path(args.config).expanduser()
    else:
        candidates = [
            Path.cwd() / f"{theme_name}_configuration.yaml",
            Path.cwd() / "configuration.yaml",
        ]
        found = next((p for p in candidates if p.exists()), None)
        if not found:
            raise SystemExit("❌ No se encontró ningún configuration.yaml válido.")
        config_path = found

    output_dir = Path(args.output_dir or (DEFAULT_OUTPUT_ROOT / theme_name)).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    config = load_configuration(config_path)
    wanted = set(a.lower() for a in args.only) if args.only else None

    print(f"✨ Generando theme '{theme_name}' desde {config_path.name}")
    print(f"📦 Carpeta de salida → {output_dir}")

    # ───────────────────────────────
    #  Componentes con plantillas
    # ───────────────────────────────
    for spec in TEMPLATED_COMPONENTS:
        if wanted and spec.name not in wanted:
            continue
        template_path = templates_dir / spec.template_filename
        data = config.get(spec.config_key, {})
        out_path = output_dir / spec.output_filename
        generate_file_from_template(template_path, data, out_path)
        print(f"  • {spec.name}: {out_path.name}")

    # ───────────────────────────────
    #  Componentes simples
    # ───────────────────────────────
    for name, generator in SIMPLE_COMPONENTS.items():
        if wanted and name not in wanted:
            continue
        out_file = output_dir / {
            "icons": "icons.theme",
            "ghostty": "ghostty.conf",
            "neovim": "neovim.lua",
            "vscode": "vscode.json",
        }[name]
        content = generator(theme_name) if callable(generator) else generator
        out_file.write_text(str(content))
        print(f"  • {name}: {out_file.name}")

    print(f"✅ Theme '{theme_name}' generado correctamente en {output_dir}")
    return 0


if __name__ == "__main__":
    main()
