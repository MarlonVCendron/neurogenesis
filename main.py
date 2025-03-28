import tqdm_pathos
from os.path import join

from plotting.spikes_and_rates import plot_spikes_and_rates
from utils.patterns import generate_activity_patterns
from utils.initialize import initialize
from sim import SimWrapper
from params import results_dir, trials
from utils.args_config import args

if __name__ == '__main__':
  initialize()

  sim = SimWrapper(report='text', monitor_rate=False)

  patterns    = [pattern for pattern in generate_activity_patterns() for _ in range(trials)]
  if args.single_run:
    patterns    = patterns[:1]

  result_dirs = [join(results_dir, f'{i}') for i in range(len(patterns))]

  results = tqdm_pathos.starmap(sim.do_run, zip(patterns, result_dirs))

  for i, (spikes, rates) in enumerate(results):
    plot_spikes_and_rates(spikes, rates, i)
