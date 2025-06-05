#!/bin/sh

./scripts/clean.sh

latexmk -pdf -output-directory=build project.tex -f

cp build/project.pdf ./
