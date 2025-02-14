from brian2 import ms
import numpy as np

from params import break_time, stim_time
from utils.patterns import get_population_pattern

def plot_spike_trains(spike_monitors, num):
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot as plt

  for spike_mon in spike_monitors:
    neuron = spike_mon.source
    pattern = get_population_pattern(spike_mon)
    print(f'Number of {neuron.name} that fired: {np.sum(pattern)}')

    plt.subplot(len(spike_monitors), 1, spike_monitors.index(spike_mon) + 1)
    plt.plot(spike_mon.t / ms, spike_mon.i, 'ok', markersize=1)
    plt.xlabel('Time (ms)')
    plt.ylabel(f'{neuron.name} index')
    plt.xlim(break_time / ms, stim_time / ms)
    plt.ylim(0, len(neuron))
  plt.show()
  # plt.savefig(f'neurogenesis/figures/spikes_{num}.png')
  # plt.close()