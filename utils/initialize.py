from brian2 import set_device, seed, ms, defaultclock, prefs
import numpy as np
from utils.args_config import args

def initialize():
  if not args.pattern_sequence_mode:
    set_device('cpp_standalone', build_on_run=False)
    # prefs.devices.cpp_standalone.openmp_threads = 16
    # set_device('cuda_standalone', build_on_run=False)
  defaultclock.dt = 0.1 * ms
  seed(256)
  np.random.seed(256)

