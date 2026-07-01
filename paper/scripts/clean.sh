#!/bin/sh

latexmk -C -output-directory=build sn-article.tex -f

rm *-eps-converted-to.pdf