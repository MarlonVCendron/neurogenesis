from brian2 import *
import numpy as np

from params import pp_rate
from utils.patterns import generate_pattern

active_p = 0.1

# Perforant path
def create_pp(N, rate=pp_rate, active_p=active_p, name='pp', init_rates=False):

  rates = np.zeros(N) * Hz
  if init_rates:
    pattern = generate_pattern(active_p, N)
    rates = pattern * rate

  pp = PoissonGroup(N=N, rates=rates, name=name)

  return pp

def set_pp_pattern(pp, pattern, rate=pp_rate):
  rates = np.zeros(pp.N) * Hz
  rates[pattern == 1] = rate
  pp.rates = rates
