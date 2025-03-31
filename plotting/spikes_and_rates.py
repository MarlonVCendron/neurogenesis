from brian2 import *
import numpy as np
from utils.args_config import args

from params import break_time, stim_time
from utils.patterns import get_population_pattern, get_pattern_per_lamella
from utils.utils import neuron_ordering

def plot_spikes_and_rates(spike_monitors, rate_monitors, num=0, save=True, bar=False, window_width=20*ms, filename='?'):
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot as plt
  
  spike_monitors = sorted(spike_monitors, key=lambda sm: neuron_ordering.index(sm.source.name))

  plt.figure(figsize=(10, len(spike_monitors) * 3))

  for idx, spike_mon in enumerate(spike_monitors):
    neuron = spike_mon.source
    rate_mon = next(r for r in rate_monitors if r.source.name == spike_mon.source.name)
    smooth_rates = rate_mon.smooth_rate(window='flat', width=window_width) / Hz

    pattern = get_population_pattern(spike_mon)
    # per_lamella = np.sum(get_pattern_per_lamella(pattern), axis=0)
    # print(f'Number of {neuron.name} that fired: {np.sum(pattern)}. P.L.: μ: {np.mean(per_lamella)}')
    print(f'Number of {neuron.name} that fired: {np.sum(pattern)}')

    ax1 = plt.subplot(len(spike_monitors), 1, idx + 1)

    if bar:
      ax1.bar(spike_mon.t / ms, len(neuron), width=0.1, color='k')
    else:
      ax1.plot(spike_mon.t / ms, spike_mon.i, 'ok', markersize=1)
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel(f'{neuron.name} index')
    ax1.set_xlim(break_time / ms, (break_time + stim_time) / ms)
    ax1.set_ylim(0, len(neuron))

    ax2 = ax1.twinx()
    ax2.plot(rate_mon.t / ms, smooth_rates, '-r')
    ax2.set_ylabel('Firing rate (Hz)')
    ax2.set_ylim(0, max(smooth_rates) + 1) 
  if save:
    plt.savefig(f'figures/spikes_and_rates/{filename}.png')
    plt.close()
  else:
    plt.show()