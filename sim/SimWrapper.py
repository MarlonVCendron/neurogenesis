from brian2 import *
from brian2.devices import device_module

from neurogenesis.utils.utils import get_neuron
from neurogenesis.params.sim import break_time, stim_time
from neurogenesis.models.general.network import network
from neurogenesis.models.cells.ec import set_ec_pattern
from neurogenesis.utils.patterns import generate_patterns


class SimWrapper:
  def __init__(self, report=None):
    self.net = network()

    ec = get_neuron(self.net, 'ec')
    mgc = get_neuron(self.net, 'mgc')
    bc = get_neuron(self.net, 'bc')
    neurons = [ec, mgc, bc]
    self.monitors = [SpikeMonitor(neuron) for neuron in neurons]
    self.net.add(self.monitors)

    self.activate_monitors(False)
    self.net.run(break_time, report=report)
    self.activate_monitors(True)
    self.net.run(stim_time, report=report)

    device.build(run=False)
    self.device = get_device()

  def activate_monitors(self, activate=True):
    for spike_mon in self.monitors:
      spike_mon.active = activate

  def do_run(self, pattern):
    device_module.active_device = self.device

    self.device.run(
      run_args={self.net['ec'].rates: pattern},
    )

    return self.monitors