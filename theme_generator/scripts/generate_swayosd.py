from pathlib import Path
from jinja2 import Template
import yaml

def generate_swayosd(theme_yaml: Path, template_path: Path, output_path: Path):
    """Rellena la plantilla de SwayOSD con los colores definidos en el YAML."""
    data = yaml.safe_load(theme_yaml.read_text())
    template = Template(template_path.read_text())
    rendered = template.render(data)
    output_path.write_text(rendered)
    print(f"✅ Generated SwayOSD theme → {output_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    generate_swayosd(
        theme_yaml=base_dir / "swayosd.yaml",
        template_path=base_dir / "swayosd_template.css",
        output_path=base_dir / "swayosd.css"
    )
