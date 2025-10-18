from pathlib import Path
from jinja2 import Template
import yaml

def generate_mako(theme_yaml: Path, template_path: Path, output_path: Path):
    """Rellena la plantilla de Mako con los valores definidos en el YAML."""
    data = yaml.safe_load(theme_yaml.read_text())
    template = Template(template_path.read_text())
    rendered = template.render(data)
    output_path.write_text(rendered)
    print(f"✅ Generated Mako config → {output_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    generate_mako(
        theme_yaml=base_dir / "mako.yaml",
        template_path=base_dir / "mako_template.ini",
        output_path=base_dir / "mako.ini"
    )
