from brian2 import *
import numpy as np

rate = 40 * Hz

# Entorhinal cortex
def create_ec(N):

  rates = np.zeros(N) * Hz
  rates[np.random.randint(0, N, int(0.3 * N))] = rate

  ec = PoissonGroup(N=N, rates=rates, name='ec')

  return ec
