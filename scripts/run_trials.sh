#!/bin/bash

prefix=$1
trials=30

if [ -z "$prefix" ]; then
  echo "Usage: $0 <prefix>"
  exit 1
fi

if [ -z "$2" ]; then
  echo "No trials specified, using default: $trials"
else
  trials=$2
fi

echo "Running: control"
python -m main --trials $trials --prefix $prefix

for igc_conn in $(seq 0.1 0.1 1.0); do
  echo "Running: neurogenesis --igc-conn $igc_conn"
  python -m main --trials $trials --neurogenesis --igc-conn=$igc_conn --prefix $prefix
done

