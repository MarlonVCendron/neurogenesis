#!/bin/sh

./scripts/clean.sh

latexmk -pdf -output-directory=build project.tex -f

cp build/project.pdf ./
cp build/project.pdf ./Projeto\ -\ Modelo\ computacional\ sobre\ a\ dinâmica\ temporal\ da\ neurogênese\ adulta\ no\ giro\ denteado\ e\ seu\ impacto\ nas\ funções\ de\ memória\ do\ CA3.pdf 
