import tqdm_pathos
from os.path import join

from plotting.spike_trains import plot_spike_trains
from plotting.spikes_and_rates import plot_spikes_and_rates
from utils.patterns import generate_activity_patterns
from utils.initialize import initialize
from sim import SimWrapper
from params import results_dir, trials

if __name__ == '__main__':
  initialize()

  sim = SimWrapper(report='text')

  patterns    = [pattern for pattern in generate_activity_patterns() for _ in range(trials)]
  patterns    = patterns[:1]
  result_dirs = [join(results_dir, f'{i}') for i in range(len(patterns))]

  results = tqdm_pathos.starmap(sim.do_run, zip(patterns, result_dirs))

  for i, (spikes, rates) in enumerate(results):
    # plot_spike_trains(r, i)
    plot_spikes_and_rates(spikes, rates, i)
