#!/bin/bash

# for neurogenesis in true false; do
for neurogenesis in false; do
  for nmda in {11..12..1}; do
    for gaba in {2..6..1}; do
      for ampa in {2..6..1}; do
        if [[ "$neurogenesis" == "true" ]]; then
          echo "Running: python -m main --nmda $nmda --ampa $ampa --gaba $gaba --neurogenesis"
          python -m main --nmda $nmda --ampa $ampa --gaba $gaba --neurogenesis
        else
          echo "Running: python -m main --nmda $nmda --ampa $ampa --gaba $gaba"
          python -m main --nmda $nmda --ampa $ampa --gaba $gaba
        fi
      done
    done
  done
done