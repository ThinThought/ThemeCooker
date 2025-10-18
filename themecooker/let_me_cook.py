#!/usr/bin/env python3
"""Copies the configuration template from the ThemeCooker package to the current directory."""

from pathlib import Path
import shutil
import sys
import importlib.resources as resources


def main():
    try:
        # Localiza el archivo dentro del paquete
        with resources.path("themecooker.generator.config", "theme_configuration_template.yaml") as template_path:
            dest_path = Path.cwd() / "configuration.yaml"

            if dest_path.exists():
                print(f"⚠️  '{dest_path}' already exists — aborting to avoid overwrite.")
                sys.exit(1)

            shutil.copy(template_path, dest_path)
            print(f"✅ Copied configuration template → {dest_path}")

    except FileNotFoundError:
        print("❌ Could not find the template file inside the package.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
