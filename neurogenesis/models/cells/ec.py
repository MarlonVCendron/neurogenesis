from brian2 import *
import numpy as np

rate = 40 * Hz

# Entorhinal cortex
def create_ec(N):

  # Only 10% of the cells are active at random at any given time
  rates = np.zeros(N) * Hz
  rates[np.random.randint(0, N, int(0.1 * N))] = rate

  ec = PoissonGroup(N=N, rates=rates)

  return ec
