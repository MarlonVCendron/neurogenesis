import numpy as np


def gini_index(spike_counts):
    """Population sparsity via Gini index."""
    x = np.sort(np.asarray(spike_counts, dtype=float))
    N = len(x)
    total = x.sum()

    if total == 0:
        return 0.0

    i = np.arange(1, N + 1)
    return float(np.sum((2 * i - N - 1) * x) / (N * total))


def hoyer(spike_counts):
    """Population sparsity via Hoyer method."""
    x = np.asarray(spike_counts, dtype=float)
    N = len(x)

    sum_squares = np.sum(x ** 2)

    if sum_squares <= 0 or N <= 1:
      return 0.0

    return float((np.sqrt(N) - np.sum(np.abs(x)) / np.sqrt(sum_squares)) / (np.sqrt(N) - 1))
