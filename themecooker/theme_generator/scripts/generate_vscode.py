from pathlib import Path
import argparse
import re
import json


DEFAULT_THEME_NAME = "tokyonight"
SCRIPT_DIR = Path(__file__).resolve().parent

def normalize_theme_name(name: str):
    """Genera las tres variantes del nombre del theme."""
    display_name = " ".join(word.capitalize() for word in re.split(r"[-_\s]+", name))
    kebab_name = re.sub(r"[\s_]+", "-", name.lower())
    flat_name = re.sub(r"[-_\s]+", "", name.lower())
    return display_name, kebab_name, flat_name

def generate_vscode(theme_name: str, output_path: Path):
    """Genera vscode.json con nombre y extensión basados en el theme."""
    display_name, kebab_name, flat_name = normalize_theme_name(theme_name)

    data = {
        "name": display_name,
        "extension": f"{flat_name}.{kebab_name}"
    }

    output_path.write_text(json.dumps(data, indent=2))
    print(f"✅ Generated VSCode config → {output_path}")
    print(f"📛 name: {display_name}\n📦 extension: {data['extension']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate VSCode theme config")
    parser.add_argument(
        "theme_name",
        nargs="?",
        default=DEFAULT_THEME_NAME,
        help="Base name of the theme (default: tokyonight)",
    )
    parser.add_argument(
        "--output",
        default=str(SCRIPT_DIR / "vscode.json"),
        help="Output file (default: vscode.json next to this script)",
    )
    args = parser.parse_args()

    generate_vscode(args.theme_name, Path(args.output).expanduser())
