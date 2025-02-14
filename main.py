import tqdm_pathos
from os.path import join

from neurogenesis.plotting.spike_trains import plot_spike_trains
from neurogenesis.utils.patterns import generate_activity_patterns
from neurogenesis.utils.initialize import initialize
from neurogenesis.sim import SimWrapper
from neurogenesis.params import results_dir, trials

if __name__ == '__main__':
  initialize()

  sim = SimWrapper()

  patterns    = [pattern for pattern in generate_activity_patterns() for _ in range(trials)]
  patterns    = patterns[:2]
  result_dirs = [join(results_dir, f'{i}') for i in range(len(patterns))]

  results = tqdm_pathos.starmap(sim.do_run, zip(patterns, result_dirs))

  for i, r in enumerate(results):
    plot_spike_trains(r, i)
