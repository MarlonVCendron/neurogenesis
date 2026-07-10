#!/bin/sh

./scripts/clean.sh

BSTINPUTS=./bst: latexmk -pdf -pdflatex="pdflatex" -output-directory=build sn-article.tex -f

mv build/sn-article.pdf ./

latexmk -pdf -pdflatex="pdflatex" -output-directory=build online-resource-1.tex -f

mv build/online-resource-1.pdf ./

./scripts/clean.sh