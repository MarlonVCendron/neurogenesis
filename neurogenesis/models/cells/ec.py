from brian2 import *

rate = 40 * Hz


def create_ec(N):

  ec = PoissonGroup(N=N, rates=rate)

  return ec
