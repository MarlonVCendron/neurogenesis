from brian2 import *
import numpy as np

from params import break_time, stim_time
from utils.patterns import get_population_pattern

def plot_spikes_and_rates(spike_monitors, rate_monitors, num):
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot as plt

  plt.figure(figsize=(10, len(spike_monitors) * 3))

  for idx, spike_mon in enumerate(spike_monitors):
    neuron = spike_mon.source
    rate_mon = next(r for r in rate_monitors if r.source.name == spike_mon.source.name)
    smooth_rates = rate_mon.smooth_rate(window='flat', width=100 * ms) / Hz

    pattern = get_population_pattern(spike_mon)
    print(f'Number of {neuron.name} that fired: {np.sum(pattern)}')

    ax1 = plt.subplot(len(spike_monitors), 1, idx + 1)

    ax1.plot(spike_mon.t / ms, spike_mon.i, 'ok', markersize=1)
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel(f'{neuron.name} index')
    ax1.set_xlim(break_time / ms, stim_time / ms)
    ax1.set_ylim(0, len(neuron))

    ax2 = ax1.twinx()
    ax2.plot(rate_mon.t / ms, smooth_rates, '-r')
    ax2.set_ylabel('Firing rate (Hz)')
    ax2.set_ylim(0, max(smooth_rates) + 1) 
  # plt.show()
  plt.savefig(f'figures/rates_experiments/?.png')
  plt.close()