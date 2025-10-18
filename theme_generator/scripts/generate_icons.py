from pathlib import Path
import argparse

def generate_icons(theme_name: str, output_path: Path):
    """Genera icons.theme con el nombre del tema indicado."""
    output_path.write_text(f"{theme_name}\n")
    print(f"✅ Generated icons.theme → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate icon theme config")
    parser.add_argument("theme_name", help="Name of the icon theme (e.g., Yaru-magenta)")
    parser.add_argument(
        "--output",
        default="icons.theme",
        help="Output path for the icon theme file (default: icons.theme)"
    )
    args = parser.parse_args()

    generate_icons(args.theme_name, Path(args.output))
