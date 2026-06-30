#!/bin/sh

./scripts/clean.sh

BSTINPUTS=./bst: latexmk -pdf -pdflatex="pdflatex" -output-directory=build sn-article.tex -f

mv build/sn-article.pdf ./

./scripts/clean.sh