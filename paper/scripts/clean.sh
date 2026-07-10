#!/bin/sh

latexmk -C -output-directory=build sn-article.tex -f

latexmk -C -output-directory=build online-resource-1.tex -f

rm -f *-eps-converted-to.pdf