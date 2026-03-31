import numpy as np
from utils.patterns import get_population_spike_counts


def gini_index(monitor):
    """Population sparsity via Gini index."""
    x = np.sort(get_population_spike_counts(monitor)).astype(float)
    N = len(x)
    total = x.sum()

    if total == 0:
        return 0.0

    i = np.arange(1, N + 1)
    return float(np.sum((2 * i - N - 1) * x) / (N * total))


def hoyer(monitor):
    """Population sparsity via Hoyer method."""
    x = get_population_spike_counts(monitor).astype(float)
    N = len(x)

    sum_squares = np.sum(x ** 2)

    if sum_squares <= 0 or N <= 1:
      return 0.0

    return float((np.sqrt(N) - np.sum(np.abs(x)) / np.sqrt(sum_squares)) / (np.sqrt(N) - 1))
