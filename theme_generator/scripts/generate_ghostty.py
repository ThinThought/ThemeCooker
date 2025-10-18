from pathlib import Path
import argparse

def generate_ghostty(theme_name: str, output_path: Path):
    """Genera el archivo ghostty.conf con el nombre del tema indicado."""
    content = f"theme = {theme_name}\n"
    output_path.write_text(content)
    print(f"✅ Generated Ghostty config → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Ghostty theme config")
    parser.add_argument("theme_name", help="Name of the theme (e.g., TokyoNight)")
    parser.add_argument(
        "--output",
        default="ghostty.conf",
        help="Output path for the config file (default: ghostty.conf)"
    )
    args = parser.parse_args()

    generate_ghostty(args.theme_name, Path(args.output))
