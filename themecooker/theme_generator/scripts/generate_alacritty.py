from pathlib import Path
from jinja2 import Template
import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
YAML_DIR = ROOT_DIR / "yaml"
TEMPLATE_DIR = ROOT_DIR / "templates"


def generate_alacritty(theme_yaml: Path, template_path: Path, output_path: Path):
    """Rellena la plantilla de Alacritty con los colores definidos en el YAML."""
    data = yaml.safe_load(theme_yaml.read_text())
    template = Template(template_path.read_text())
    rendered = template.render(data)
    output_path.write_text(rendered)
    print(f"✅ Generated Alacritty config → {output_path}")


if __name__ == "__main__":
    generate_alacritty(
        theme_yaml=YAML_DIR / "alacritty.yaml",
        template_path=TEMPLATE_DIR / "alacritty_template.toml",
        output_path=SCRIPT_DIR / "alacritty.toml",
    )
