#!/bin/bash

for neurogenesis in false true; do
  if [[ "$neurogenesis" == "false" ]]; then
    echo "Running: control"
    python -m main --trials=30
  else
    echo "Running: neurogenesis"
    python -m main --trials=30 --neurogenesis
  fi
done
