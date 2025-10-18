from pathlib import Path
import argparse

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
    parser.add_argument("theme_name", help="Name of the theme (e.g., tokyonight)")
    parser.add_argument(
        "--output",
        default="neovim.lua",
        help="Output path for the Lua config file (default: neovim.lua)"
    )
    args = parser.parse_args()

    generate_neovim(args.theme_name, Path(args.output))
