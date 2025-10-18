from pathlib import Path
import argparse


DEFAULT_THEME_NAME = "tokyonight"
SCRIPT_DIR = Path(__file__).resolve().parent

def generate_icons(theme_name: str, output_path: Path):
    """Genera icons.theme con el nombre del tema indicado."""
    output_path.write_text(f"{theme_name}\n")
    print(f"✅ Generated icons.theme → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate icon theme config")
    parser.add_argument(
        "theme_name",
        nargs="?",
        default=DEFAULT_THEME_NAME,
        help="Name of the icon theme (default: tokyonight)",
    )
    parser.add_argument(
        "--output",
        default=str(SCRIPT_DIR / "icons.theme"),
        help="Output path for the icon theme file (default: icons.theme next to this script)",
    )
    args = parser.parse_args()

    generate_icons(args.theme_name, Path(args.output).expanduser())
