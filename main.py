import tqdm_pathos
from os.path import join

from plotting.spikes_and_rates import plot_spikes_and_rates
from utils.patterns import generate_activity_patterns
from utils.initialize import initialize
from sim import SimWrapper
from params import results_dir, trials
from utils.args_config import args

def res_filename(i, total):
  patterns_per_trial = total // trials
  trial_index = i // patterns_per_trial
  pattern_index = i % patterns_per_trial
  flag = 'neurogenesis' if args.neurogenesis else 'control'
  return f'{args.prefix}_{flag}_trial_{trial_index}_pattern_{pattern_index}'

if __name__ == '__main__':
  initialize()

  monitor_rate = True
  sim = SimWrapper(report='text', monitor_rate=monitor_rate)

  patterns    = [pattern for _ in range(trials) for pattern in generate_activity_patterns()]
  if args.single_run:
    patterns    = patterns[:1]

  total_patterns = len(patterns)
  result_dirs = [join(results_dir, res_filename(i, total_patterns)) for i in range(total_patterns)]

  results = tqdm_pathos.starmap(sim.do_run, zip(patterns, result_dirs))

  if(monitor_rate):
    for i, (spikes, rates) in enumerate(results):
      plot_spikes_and_rates(spikes, rates, i, filename=res_filename(i, total_patterns))
