from pathlib import Path
import yaml
from jinja2 import Template


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
YAML_DIR = ROOT_DIR / "yaml"
TEMPLATE_DIR = ROOT_DIR / "templates"

def generate_waybar(theme_yaml: Path, template_path: Path, output_path: Path):
    """Rellena la plantilla de Waybar con los colores definidos en el YAML."""
    data = yaml.safe_load(theme_yaml.read_text())
    template = Template(template_path.read_text())
    rendered = template.render(data)
    output_path.write_text(rendered)
    print(f"✅ Generated Waybar theme → {output_path}")

if __name__ == "__main__":
    generate_waybar(
        theme_yaml=YAML_DIR / "waybar.yaml",
        template_path=TEMPLATE_DIR / "waybar_template.css",
        output_path=SCRIPT_DIR / "waybar.css",
    )
