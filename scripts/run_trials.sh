#!/bin/bash

echo "Running: control"
python -m main --trials=30

echo "Running: neurogenesis"
python -m main --trials=30 --neurogenesis
