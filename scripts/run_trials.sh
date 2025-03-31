#!/bin/bash

prefix="run_02"
trials=30

echo "Running: control"
python -m main --trials $trials --prefix $prefix

for igc_conn in $(seq 0.1 0.1 1.0); do
  echo "Running: neurogenesis --igc-conn $igc_conn"
  python -m main --trials $trials --neurogenesis --igc-conn=$igc_conn
done

