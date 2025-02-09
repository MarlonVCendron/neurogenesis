from brian2 import *
import numpy as np

rate = 40 * Hz
active_p = 0.1

# Entorhinal cortex
def create_ec(N, rate=rate, active_p=active_p, name='ec'):

  active_neurons = np.random.choice(range(N), size=int(N*active_p), replace=False)

  rates = np.zeros(N) * Hz
  rates[active_neurons] = rate

  ec = PoissonGroup(N=N, rates=rates, name=name)

  return (ec, active_neurons)

def set_ec_pattern(ec, pattern, rate=rate):
  rates = np.zeros(ec.N) * Hz
  rates[pattern == 1] = rate
  ec.rates = rates
