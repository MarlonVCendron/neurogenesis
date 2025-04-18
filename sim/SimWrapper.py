from brian2 import *

from utils.utils import get_spike_monitors, get_neuron_monitor, get_neurons, get_rate_monitors
from utils.save_to_file import save_to_file
from utils.patterns import get_population_pattern
from params import break_time, stim_time
from models.general.network import network
from plotting.connectivity_matrices import connectivity_matrices
from utils.args_config import args

class SimWrapper:
  def __init__(self, monitor_rate=True, report=None):
    self.net = network()

    neurons = get_neurons(self.net)
    spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]
    rate_monitors = [PopulationRateMonitor(neuron) for neuron in neurons] if monitor_rate else []
    self.monitors = spike_monitors + rate_monitors
    self.net.add(self.monitors)

    self.activate_monitors(False)
    self.net.run(break_time, report=report)
    self.activate_monitors(True)
    self.net.run(stim_time, report=report)

    device.build(run=False)
    self.device = get_device()

  def activate_monitors(self, activate=True):
    for mon in self.monitors:
      mon.active = activate
    
  def save_results(self, pattern, results_directory):
    mgc_pattern = get_population_pattern(get_neuron_monitor(self.net, 'mgc'))
    igc_pattern = get_population_pattern(get_neuron_monitor(self.net, 'igc'))
    save_to_file(results_directory, pattern, mgc_pattern, igc_pattern)

  def do_run(self, pattern, results_directory):
    from brian2.devices import device_module
    device_module.active_device = self.device

    self.device.run(
        results_directory=results_directory,
        run_args={self.net['pp'].rates: pattern['rates']}
    )

    if args.generate_graph:
      connectivity_matrices(self.net)

    self.save_results(pattern, results_directory)

    return (get_spike_monitors(self.net), get_rate_monitors(self.net))
