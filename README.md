# ThemeCooker

ThemeCooker or Theme Cooker, es una app que se me ha ocurrido para semi-auto-generar themes para omarchy, en base a 
backgrounds que se pasen como input para el theme.

Debemos partir de un template theme y luego afinar hacia lo que queremos conseguir.

# Setup

I am going to give a try to UV python from astral.

## Install
```bash
pip install .
```

## Commands

### let-me-cook
Gives you a cook-theme_template.yaml with every value with null. You do what you want. 

```bash
let-me-cook
```


Also in this repository I am working on how to extract a color code for a theme based on the backgrounds


### cook-theme

You can cook your own theme

```bash
export theme_name="tokyonight"
cook-theme --config tokyonight_config.yaml \
           --output-dir "./$theme_name" \
           "$theme_name"
```

## Theme generator
I am trying to automate the theme creation taking images and extracting color schemes.

I want to later use those color schemes to generate a theme using templates, taking input data from yaml and using python to process that.

