from brian2 import *

rate = 40 * Hz

# Entorhinal cortex
def create_ec(N):

  ec = PoissonGroup(N=N, rates=rate)

  return ec
