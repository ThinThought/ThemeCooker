from pathlib import Path
import yaml
from jinja2 import Template


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
YAML_DIR = ROOT_DIR / "yaml"
TEMPLATE_DIR = ROOT_DIR / "templates"

def generate_hyprland(theme_yaml: Path, template_path: Path, output_path: Path):
    """Rellena la plantilla de Hyprland con los valores definidos en el YAML."""
    data = yaml.safe_load(theme_yaml.read_text())
    template = Template(template_path.read_text())
    rendered = template.render(data)
    output_path.write_text(rendered)
    print(f"✅ Generated Hyprland config → {output_path}")

if __name__ == "__main__":
    generate_hyprland(
        theme_yaml=YAML_DIR / "hyprland.yaml",
        template_path=TEMPLATE_DIR / "hyprland_template.conf",
        output_path=SCRIPT_DIR / "hyprland.conf",
    )
