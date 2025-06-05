#!/bin/bash

echo "Cleaning up"
rm -rf /home/marlon/edu/mestrado/proj/neurogenesis/connectivity/*

echo "Running: control"
python -m scripts.generate_connectivity_matrices --skip-connectivity-matrices --ca3

for igc_conn in $(seq 0.1 0.1 1.0); do
  echo "Running: neurogenesis --igc-conn $igc_conn"
  python -m scripts.generate_connectivity_matrices --skip-connectivity-matrices --neurogenesis --ca3 --igc-conn=$igc_conn
done
