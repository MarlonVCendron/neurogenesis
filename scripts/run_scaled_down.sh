#!/bin/bash

ARGS="\
  --single-run \
  --ca3 \
  --neurogenesis \
  --igc-conn=0.5 \
  --skip-connectivity-matrices \
  --generate-graph \
  --break-time=1 \
  --stim-time=1 \
  --n-lamellae=4 \
  --n-pp=20 \
  --n-mgc=25 \
  --n-igc=4 \
  --n-bc=1 \
  --n-mc=2 \
  --n-hipp=1 \
  --n-pca3=6 \
  --n-ica3=1"

python -m main $ARGS

echo "Running graph export script..."
python -m scripts.graph_export $ARGS