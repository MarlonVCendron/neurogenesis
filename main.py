from brian2 import set_device, seed, ms, defaultclock
import tqdm_pathos
from os.path import join
import numpy as np

from neurogenesis.plotting.spike_trains import plot_spike_trains
from neurogenesis.utils.patterns import generate_activity_patterns
from neurogenesis.sim import SimWrapper

base_dir = './neurogenesis'
results_dir = join(base_dir, 'res')

if __name__ == '__main__':
  set_device('cpp_standalone', build_on_run=False)

  defaultclock.dt = 0.1 * ms
  seed(256)
  np.random.seed(256)

  trials = 1  # 30

  sim = SimWrapper()

  patterns = [pattern for pattern in generate_activity_patterns() for _ in range(trials)]
  patterns = [patterns[0], patterns[8]]
  result_dirs = [join(results_dir, f'{i}') for i in range(len(patterns))]

  results = tqdm_pathos.starmap(sim.do_run, zip(patterns, result_dirs))
  
  for i, r in enumerate(results):
    plot_spike_trains(r, i)
