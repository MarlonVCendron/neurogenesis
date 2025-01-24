# Condition to connect cells in lamellae
def lamellar_conn(N_i, N_j):
  return f'i // {N_i} == j // {N_j}'

# Condition to connect cells cross lamellae
def cross_lamellar_conn(N_i, N_j):
  return f'i // {N_i} != j // {N_j}'