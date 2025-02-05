from brian2 import *

from neurogenesis.utils.utils import get_neurons
from neurogenesis.params.sim import break_time, stim_time

def plot_spike_trains(net, spike_monitors):
  neurons = get_neurons(net)
  
  for (i, spike_mon) in enumerate(spike_monitors):
    print(f'Number of {neurons[i].name} that fired: {len(set(spike_mon.i))}')

    plt.subplot(len(spike_monitors), 1, spike_monitors.index(spike_mon) + 1)
    plt.plot(spike_mon.t / ms, spike_mon.i, 'ok', markersize=1)
    plt.xlabel('Time (ms)')
    plt.ylabel(f'{neurons[i].name} index')
    plt.xlim(break_time / ms, stim_time / ms)
    plt.ylim(0, len(neurons[i]))
  plt.show()
  # plt.savefig('neurogenesis/figures/spikes.png')
  # plt.close()