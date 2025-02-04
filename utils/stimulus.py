from neurogenesis.params.cells import cell_params
import numpy as np

p = 0.1
N = cell_params['ec']['N']

# Creates a binary pattern of active neurons
def generate_pattern(p=p, N=N):
  indices = np.random.choice(N, int(N*p), replace=False)
  pattern = np.zeros(N, dtype=int)
  pattern[indices] = 1
  return pattern

def generate_similar_patterns(pattern, step=0.1):
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

def pattern_similarity(a, b):
  # not this
  return np.sum(a == b) / len(a)

pattern = generate_pattern(0.1, 400)
patterns = generate_similar_patterns(pattern)

print(pattern)
print('---')
for p in patterns:
  # print(len(np.where(p == 1)[0]))
  # print(p)
  print(pattern_similarity(pattern, p))


