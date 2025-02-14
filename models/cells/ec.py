from brian2 import *
import numpy as np

from params import ec_rate
from utils.patterns import generate_pattern

active_p = 0.1

# Entorhinal cortex
def create_ec(N, rate=ec_rate, active_p=active_p, name='ec', init_rates=False):

  rates = np.zeros(N) * Hz
  if init_rates:
    pattern = generate_pattern(active_p, N)
    rates = pattern * rate

  ec = PoissonGroup(N=N, rates=rates, name=name)

  return ec

def set_ec_pattern(ec, pattern, rate=ec_rate):
  rates = np.zeros(ec.N) * Hz
  rates[pattern == 1] = rate
  ec.rates = rates
