from pathlib import Path
import yaml
from jinja2 import Template


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
YAML_DIR = ROOT_DIR / "yaml"
TEMPLATE_DIR = ROOT_DIR / "templates"

def generate_chromium(theme_yaml: Path, template_path: Path, output_path: Path):
    """Rellena la plantilla de Chromium con los colores definidos en el YAML."""
    data = yaml.safe_load(theme_yaml.read_text())
    template = Template(template_path.read_text())
    rendered = template.render(data)
    output_path.write_text(rendered)
    print(f"✅ Generated Chromium theme → {output_path}")

if __name__ == "__main__":
    generate_chromium(
        theme_yaml=YAML_DIR / "chromium.yaml",
        template_path=TEMPLATE_DIR / "chromium_template.theme",
        output_path=SCRIPT_DIR / "chromium.theme",
    )
