from pathlib import Path
import argparse


DEFAULT_THEME_NAME = "tokyonight"
SCRIPT_DIR = Path(__file__).resolve().parent

def generate_ghostty(theme_name: str, output_path: Path):
    """Genera el archivo ghostty.conf con el nombre del tema indicado."""
    content = f"theme = {theme_name}\n"
    output_path.write_text(content)
    print(f"✅ Generated Ghostty config → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Ghostty theme config")
    parser.add_argument(
        "theme_name",
        nargs="?",
        default=DEFAULT_THEME_NAME,
        help="Name of the theme (default: tokyonight)",
    )
    parser.add_argument(
        "--output",
        default=str(SCRIPT_DIR / "ghostty.conf"),
        help="Output path for the config file (default: ghostty.conf next to this script)",
    )
    args = parser.parse_args()

    generate_ghostty(args.theme_name, Path(args.output).expanduser())
