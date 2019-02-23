# Udacity DataAnalyst NanoDegree

This repository contains the projects I created for the Udacity DataAnalyst NanoDegree.
Additionally there is a LaTex template file, I'm using to create my reports.
I've orginally adopted this template file from https://github.com/Wandmalfarbe/pandoc-latex-template and modified it for my needs.

## PDF Build Instructions

I'm doing code highlighting using [Pandoc Minted](https://pypi.org/project/pandoc-minted/) instead of the default markdown highlighting. This enables different background colors and more flexible syntax highlighting without having issues with LaTex.

Moreover I created a script to convert the __Jupyter Notebook Markdown Export__ to a nice file for my Use-Case and automate the whole Build-Process from markdown to pdf.
Therefore I need several tools:

__Install pandoc-minted and pypandoc__
```bash
pip install pandoc-minted
pip install pypandoc

```

__Install imgkit:__
```bash
pip install imgkit
```


__Build PDF:__

```bash
pandoc --standalone --number-sections --filter pandoc-minted \
       -o 01_explore_weather_trends.tex --template=../eisvogel.tex \
       --toc 01_explore_weather_trends.md \
       -V toc-own-page=true -V titlepage=true -V urlcolor=cyan \
       && pdflatex -interaction=nonstopmode -shell-escape 01_explore_weather_trends.tex
```

__OR__ the script __modify_and_build_pdf.py__ will do it for you.
