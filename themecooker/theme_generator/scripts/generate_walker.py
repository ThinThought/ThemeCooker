from pathlib import Path
import yaml
from jinja2 import Template


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
YAML_DIR = ROOT_DIR / "yaml"
TEMPLATE_DIR = ROOT_DIR / "templates"

def generate_walker(theme_yaml: Path, template_path: Path, output_path: Path):
    """Rellena la plantilla de Walker con los colores definidos en el YAML."""
    data = yaml.safe_load(theme_yaml.read_text())
    template = Template(template_path.read_text())
    rendered = template.render(data)
    output_path.write_text(rendered)
    print(f"✅ Generated Walker theme → {output_path}")

if __name__ == "__main__":
    generate_walker(
        theme_yaml=YAML_DIR / "walker.yaml",
        template_path=TEMPLATE_DIR / "walker_template.css",
        output_path=SCRIPT_DIR / "walker.css",
    )
