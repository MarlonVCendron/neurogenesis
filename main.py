from brian2 import *
from neurogenesis.utils.utils import get_neurons, get_neuron
from neurogenesis.params.sim import break_time, stim_time
from neurogenesis.models.general.network import network
from neurogenesis.plotting.spike_trains import plot_spike_trains
from neurogenesis.models.cells.ec import set_ec_pattern
from neurogenesis.utils.patterns import generate_patterns

set_device('cpp_standalone', build_on_run=False)

defaultclock.dt = 0.1 * ms

trials = 30

def main():
  start_scope()

  net = network()

  print('Created network')

  ec = net.get_neuron(net, 'ec')
  mgc = net.get_neuron(net, 'mgc')
  spike_monitors = [ec, mgc]

  net.add(spike_monitors)

  net.store()

  for trial in range(trials):
    print(f'Trial {trial + 1} of {trials}')

    patterns = generate_patterns()
    for pattern in patterns:
      net.restore()
      set_ec_pattern(ec, pattern)

      net.run(break_time + stim_time, report='text')

  device.build()

  # plot_spike_trains(net, spike_monitors)


if __name__ == '__main__':
  main()
