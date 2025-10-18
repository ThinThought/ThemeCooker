from pathlib import Path
import argparse


DEFAULT_THEME_NAME = "tokyonight"
SCRIPT_DIR = Path(__file__).resolve().parent

def generate_neovim(theme_name: str, output_path: Path):
    """Genera neovim.lua con el nombre del tema indicado."""
    content = f"""return {{
    {{
        "LazyVim/LazyVim",
        opts = {{
            colorscheme = "{theme_name}",
        }},
    }},
}}"""
    output_path.write_text(content)
    print(f"✅ Generated Neovim config → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Neovim colorscheme config")
    parser.add_argument(
        "theme_name",
        nargs="?",
        default=DEFAULT_THEME_NAME,
        help="Name of the theme (default: tokyonight)",
    )
    parser.add_argument(
        "--output",
        default=str(SCRIPT_DIR / "neovim.lua"),
        help="Output path for the Lua config file (default: neovim.lua next to this script)",
    )
    args = parser.parse_args()

    generate_neovim(args.theme_name, Path(args.output).expanduser())
