#!/bin/bash

for neurogenesis in true false; do
  if [[ "$neurogenesis" == "false" ]]; then
    echo "Running: control"
    python -m main --trials=30
  else
    echo "Running: neurogenesis"
    python -m main --trials=30 --neurogenesis
  fi
done
