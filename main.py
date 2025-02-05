from brian2 import *
from neurogenesis.utils.utils import get_neurons
from neurogenesis.params.sim import break_time, stim_time
from neurogenesis.models.general.network import network
from neurogenesis.plotting.spike_trains import plot_spike_trains

set_device('cpp_standalone', build_on_run=False)

defaultclock.dt = 0.1 * ms

def main():
  start_scope()

  net = network()

  print('Created network')

  neurons = get_neurons(net)
  spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]

  net.add(spike_monitors)

  net.run(break_time, report='text')
  net.run(stim_time, report='text')

  device.build()

  plot_spike_trains(net, spike_monitors)


if __name__ == '__main__':
  main()
