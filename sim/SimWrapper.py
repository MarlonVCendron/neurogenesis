from brian2 import *
import numpy as np

from neurogenesis.utils.utils import get_spike_monitors, get_neuron_monitor
from neurogenesis.utils.save_to_file import save_to_file
from neurogenesis.utils.patterns import get_population_pattern
from neurogenesis.params.sim import break_time, stim_time
from neurogenesis.models.general.network import network


class SimWrapper:
  def __init__(self, report=None):
    self.net = network()

    neurons = [self.net['ec'], self.net['mgc'], self.net['bc']]
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
    
  def save_results(self, pattern, results_directory):
    mgc_pattern = get_population_pattern(get_neuron_monitor(self.net, 'mgc'))
    save_to_file(results_directory, pattern, mgc_pattern)

  def do_run(self, pattern, results_directory):
    from brian2.devices import device_module
    device_module.active_device = self.device

    self.device.run(
        results_directory=results_directory,
        run_args={self.net['ec'].rates: pattern['rates']}
    )
    
    self.save_results(pattern, results_directory)

    return get_spike_monitors(self.net)
