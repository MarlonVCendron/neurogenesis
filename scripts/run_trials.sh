#!/bin/bash

prefix=$1
trials=30
seq=$(seq 0.1 0.1 1.0)

if [ -z "$prefix" ]; then
  echo "Usage: $0 <prefix>"
  exit 1
fi

if [ -z "$2" ]; then
  echo "No trials specified, using default: $trials"
else
  trials=$2
fi

if [ -z "$3" ]; then
  echo "No seq specified, using default: $(echo $seq | tr '\n' ' ')"
else
  seq=$3
fi

echo "Running $prefix for $trials trials with igc seq $seq"

echo "Running: control"
python -m main --trials $trials --prefix $prefix --no-neurogenesis

for igc_conn in $seq; do
  echo "Running: neurogenesis --igc-conn $igc_conn"
  python -m main --trials $trials --igc-conn=$igc_conn --prefix $prefix
done

