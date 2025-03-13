# Condition to connect cells in lamellae
def lamellar_conn(N_i, N_j):
  return f'i // {N_i} == j // {N_j}'

# Condition to connect cells cross lamellae
def cross_lamellar_conn(N_i, N_j):
  return f'i // {N_i} != j // {N_j}'

# def cross_lamellar_conn(N_i, N_j):
#   return f'(abs((i // {N_i}) - (j // {N_j})) % 20 == 1)'

# def range_conn(N_i, N_j, N=20, d=4):
#   return f'(abs((i // {N_i}) - (j // {N_j})) % {N} < {d})'
