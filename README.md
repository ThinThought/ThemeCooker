# 🍳 ThemeCooker

CLI toolkit to **generate full visual themes** for Omarchy and similar Linux environments.  
Automates everything: extract → prepare → build.

---

## ⚡ Workflow

Run commands **from a working directory that contains an `images/` folder**  
(with your wallpapers or color reference images).  

```bash
theme-template                     # 1. Create base config template
theme-extract                      # 2. Extract color palette from images/
theme-prepare my_theme             # 3. Merge palette + template
theme-build my_theme_configuration.yaml  # 4. Generate theme folder
````

Checkout the extracted color palette with:

```bash
theme-analyze my_theme_configuration.yaml
```


---

## 🧩 Commands

| Command                     | Description                                                                      |
| --------------------------- | -------------------------------------------------------------------------------- |
| `theme-template`            | Create `template_configuration.yaml`                                             |
| `theme-extract`             | Extract colors from `images/` → `colors_extracted.yaml` + preview                |
| `theme-prepare <name>`      | Combine palette + template → `<name>_configuration.yaml`                         |
| `theme-build <config.yaml>` | Build all theme assets (kitty, waybar, etc.) and copy `images/` → `backgrounds/` |
| `theme-analyze <file>`      | Inspect an existing config and map colors                                        |

---

## 📁 Example Output

```
embention/
├── alacritty.toml
├── kitty.conf
├── waybar.css
├── mako.ini
├── icons.theme
└── backgrounds/
    ├── bg1.png
    └── bg2.png
```

---

## 🧱 Built For

* Omarchy & Hyprland setups
* Fast theme prototyping
* CI/CD automation of color schemes

---

**by Daiego43 / ThinThought — 2025**
