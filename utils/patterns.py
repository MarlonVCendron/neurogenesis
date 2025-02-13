from neurogenesis.params.cells import cell_params
from neurogenesis.params.general import ec_rate
import numpy as np

p = 0.1
N = cell_params['ec']['N']
step = 0.1

# Creates a binary pattern of active neurons
def generate_pattern(p=p, N=N):
  indices = np.random.choice(N, round(N*p), replace=False)
  pattern = np.zeros(N, dtype=int)
  pattern[indices] = 1
  return pattern

# Generates similar patterns
def generate_similar_patterns(pattern, step=step):
  N = len(pattern)
  patterns = []
  for overlap_p in np.arange(step, 1.0, step):
    one_indices = np.where(pattern == 1)[0]
    zero_indices = np.where(pattern == 0)[0]

    active_n = len(one_indices)

    keep_num = round(overlap_p * active_n)
    new_num = active_n - keep_num

    keep_ones = np.random.choice(one_indices, keep_num, replace=False)
    new_ones = np.random.choice(zero_indices, new_num, replace=False)

    new_pattern = np.zeros(N, dtype=int)
    new_pattern[keep_ones] = 1
    new_pattern[new_ones] = 1

    patterns.append(new_pattern)

  return patterns

# Returns a list of patterns with increasing similarity to the original pattern, which is the last element
def generate_patterns(p=p, N=N, step=step):
  pattern = generate_pattern(p, N)
  similar_patterns = generate_similar_patterns(pattern, step)
  similar_patterns.append(pattern)
  return similar_patterns

# Generates activity patterns
def generate_activity_patterns(rate=ec_rate):
  return generate_patterns() * rate

# Percentage of active neurons in a pattern
def activation_degree(pattern):
  return np.mean(pattern)

# Average activation degree between two patterns
def average_activation_degree(a, b):
  d_a = activation_degree(a)
  d_b = activation_degree(b)
  return np.mean([d_a, d_b])

# Pearson correlation coefficient between two patterns
def correlation_degree(a, b):
  correlation_matrix = np.corrcoef(a, b)
  pearson_correlation = correlation_matrix[0, 1]
  return pearson_correlation

# Orthogonalization degree between two patterns (How dissimilar they are)
def orthogonalization_degree(a, b):
  correlation = correlation_degree(a, b)
  return (1 - correlation) / 2

# Distance between two patterns
def pattern_distance(a, b):
  avg_ad = average_activation_degree(a, b)

  if(avg_ad == 0):
    return float("inf")

  return orthogonalization_degree(a, b) / avg_ad

# Pattern separation degree given two input patterns and two output patterns
def pattern_separation_degree(in_1, in_2, out_1, out_2):
  in_distance = pattern_distance(in_1, in_2)
  out_distance = pattern_distance(out_1, out_2)

  if(in_distance == 0):
    return float("inf")

  return out_distance / in_distance 
