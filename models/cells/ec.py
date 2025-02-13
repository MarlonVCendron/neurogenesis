from brian2 import *
import numpy as np
from neurogenesis.params.general import ec_rate

active_p = 0.1

# Entorhinal cortex
def create_ec(N, rate=0*Hz, active_p=active_p, name='ec'):

  active_neurons = np.random.choice(range(N), size=int(N*active_p), replace=False)

  rates = np.zeros(N) * Hz
  rates[active_neurons] = rate

  ec = PoissonGroup(N=N, rates=rates, name=name)

  return (ec, active_neurons)

def set_ec_pattern(ec, pattern, rate=ec_rate):
  rates = np.zeros(ec.N) * Hz
  rates[pattern == 1] = rate
  ec.rates = rates
