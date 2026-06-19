#!/bin/bash

prefix=$1
trials=10
# seq=$(seq 0.1 0.1 1.0)
# seq='0.2 0.5 1.0'
seq='0.3 0.4 0.6 0.7 0.8 0.9'

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

prefix_pos="${prefix}_positive"
prefix_neg="${prefix}_negative"

for igc_conn in $seq; do
  echo "Running: $prefix_pos --igc-conn $igc_conn"
  python -m main --trials $trials --igc-conn=$igc_conn --prefix $prefix_pos --optogenetics --stim-time 600 --random
done

# for igc_conn in $seq; do
#   echo "Running: $prefix_neg --igc-conn $igc_conn"
#   python -m main --trials $trials --igc-conn=$igc_conn --prefix $prefix_neg --optogenetics-neg --stim-time 600 --random
# done

