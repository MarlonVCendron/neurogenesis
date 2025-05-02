from brian2 import set_device, seed, ms, defaultclock
import numpy as np

def initialize():
  set_device('cpp_standalone', build_on_run=False)
  # set_device('cuda_standalone', build_on_run=False)
  defaultclock.dt = 0.1 * ms
  seed(256)
  np.random.seed(256)

