from brian2 import *
import tqdm_pathos
import matplotlib.pyplot as plt
from pathos.multiprocessing import ProcessingPool
from os.path import join
import numpy as np

from neurogenesis.plotting.spike_trains import plot_spike_trains
from neurogenesis.utils.patterns import generate_activity_patterns
from neurogenesis.sim import SimWrapper


base_dir = './'
results_dir = join(base_dir, 'res')

def main():
  set_device('cpp_standalone', build_on_run=False)

  seed(256)
  np.random.seed(256)
  defaultclock.dt = 0.1 * ms

  trials = 1  # 30

  sim = SimWrapper()

  patterns = [pattern for pattern in generate_activity_patterns() for _ in range(trials)]

  spike_monitors = tqdm_pathos.map(sim.do_run, patterns)
  
  for i, r in enumerate(spike_monitors):
    plot_spike_trains(r, i)

if __name__ == '__main__':
  main()
