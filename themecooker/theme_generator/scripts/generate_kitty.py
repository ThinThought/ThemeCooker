from pathlib import Path
import yaml
from jinja2 import Template


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
YAML_DIR = ROOT_DIR / "yaml"
TEMPLATE_DIR = ROOT_DIR / "templates"

def generate_kitty(theme_yaml: Path, template_path: Path, output_path: Path):
    """Rellena la plantilla de Kitty con los colores definidos en el YAML."""
    data = yaml.safe_load(theme_yaml.read_text())
    template = Template(template_path.read_text())
    rendered = template.render(data)
    output_path.write_text(rendered)
    print(f"✅ Generated Kitty theme → {output_path}")

if __name__ == "__main__":
    generate_kitty(
        theme_yaml=YAML_DIR / "kitty.yaml",
        template_path=TEMPLATE_DIR / "kitty_template.conf",
        output_path=SCRIPT_DIR / "kitty.conf",
    )
