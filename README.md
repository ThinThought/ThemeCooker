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

## Theme generator
I am trying to automate the theme creation taking images and extracting color schemes.

I want to later use those color schemes to generate a theme using templates, taking input data from yaml and using python to process that.

```mermaid
graph TD
    subgraph theme generator
        subgraph s[scripts]
        
        end
        subgraph t[templates]
        
        end
        subgraph y[yaml]
        
        end            
        
        t -. used by .-> s 
        y -. used by .-> s
    end
    
    subgraph theme generated
        subgraph backgrounds 
            img.png
        end
        tf[theme_file]
    end
    
    s -- theme file generation --> tf
    
    th[theme file]
    
    
    s1[new.sh] 
    th -.-> s1
    s1 --generates file --> s
    s1 --generates file --> t
    s1 --generates file --> y
```