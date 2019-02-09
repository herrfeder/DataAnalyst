# Udacity DataAnalyst NanoDegree

This repository contains the projects I created for the Udacity DataAnalyst NanoDegree.
Additionally there is a LaTex template file, I'm using to create my reports.
I've orginally adopted this template file from https://github.com/Wandmalfarbe/pandoc-latex-template and modified it for my needs.

## PDF Build Instructions

I'm doing code highlighting using [Pandoc Minted](https://pypi.org/project/pandoc-minted/) instead of the default markdown highlighting. This enables different background colors and more flexible syntax highlighting without having issues with LaTex.

__Install pandoc minted:__
```bash
pip install pandoc-minted
```

__Build PDF:__

```bash
pandoc --standalone --number-sections --filter pandoc-minted \
       -o 01_explore_weather_trends.tex --template=../eisvogel.tex \
       --toc 01_explore_weather_trends.md \
       -V toc-own-page=true -V titlepage=true -V urlcolor=cyan \
       && pdflatex -interaction=nonstopmode -shell-escape 01_explore_weather_trends.tex
```
