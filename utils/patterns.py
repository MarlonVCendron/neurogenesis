import math
from brian2 import Hz
from params.cells import cell_params
from params import pp_rate, break_time, N_lamellae, active_p as global_active_p
import numpy as np

# Creates a binary pattern of active neurons
def generate_pattern(p, N):
  indices = np.random.choice(N, round(N*p), replace=False)
  pattern = np.zeros(N, dtype=int)
  pattern[indices] = 1
  return pattern

# Generates similar patterns
def generate_similar_patterns(pattern, step):
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
def generate_patterns(p, N, step):
  pattern = generate_pattern(p, N)
  similar_patterns = generate_similar_patterns(pattern, step)
  similar_patterns.append(pattern)
  return similar_patterns

# Generates activity patterns
def generate_activity_patterns(active_p=global_active_p, pp_hz=pp_rate, step=0.1):
  N = cell_params['pp']['N']
  return [
    {
      'rates': pattern * pp_hz,
      'similarity': (i+1) * step,
    }
    for i, pattern in enumerate(generate_patterns(p=active_p, N=N, step=step))
  ]

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
    print('Warning: avg_ad is 0')
    return float("inf")

  return orthogonalization_degree(a, b) / avg_ad

# Pattern separation degree given two input patterns and two output patterns
def pattern_separation_degree(in_1, in_2, out_1, out_2):
  in_distance = pattern_distance(in_1, in_2)
  out_distance = pattern_distance(out_1, out_2)

  if(in_distance == 0):
    print('Warning: in_distance is 0')
    return out_distance

  return out_distance / in_distance 

# Pattern integration degree given two input patterns and two output patterns
def pattern_integration_degree(in_1, in_2, out_1, out_2):
  in_correlation = correlation_degree(in_1, in_2)
  out_correlation = correlation_degree(out_1, out_2)

  if(math.isnan(out_correlation) or math.isnan(in_correlation)):
    return 0
  
  if(math.isinf(out_correlation) or math.isinf(in_correlation)):
    return 0

  if(in_correlation < 0.0001 and in_correlation > -0.0001):
    return 0

  return out_correlation / in_correlation 

# Calculates the pattern of active cells in a population of neurons given a spike monitor
def get_population_pattern(monitor):
  if not monitor:
    return np.zeros(0, dtype=int)

  neurons = monitor.source
  pattern = np.zeros(len(neurons), dtype=int)
  for i, t in zip(monitor.i, monitor.t):
    if t > break_time:
      pattern[i] = 1
  return pattern

def get_pp_pattern(pattern):
  return np.where(pattern['rates'] > 0, 1, 0)

def get_pattern_per_lamella(pattern):
  cells_per_lamella = len(pattern) / N_lamellae
  if(cells_per_lamella == 0):
    return np.zeros(len(pattern), dtype=int)
  return np.split(pattern, cells_per_lamella)