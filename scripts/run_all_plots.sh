#!/bin/bash

python -m scripts.data.avg_activity_broken
python -m scripts.data.avg_activity_ca3
# python -m scripts.data.avg_activity
python -m scripts.data.avg_pattern_integration
python -m scripts.data.avg_pattern_separation
python -m scripts.data.firing_rate_distribution
python -m scripts.data.firing_rate_histogram
python -m scripts.data.pattern_integration
python -m scripts.data.pattern_separation
python -m scripts.data.pattern_separation_ca3
python -m scripts.data.pattern_separation_cosine
python -m scripts.data.pattern_separation_hamming
python -m scripts.data.pattern_separation_overlap
python -m scripts.data.sparsity