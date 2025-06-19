from brian2 import *

from utils.utils import (
    get_spike_monitors,
    get_rate_monitors,
    get_state_monitors,
    get_neurons,
    get_neuron_monitor,
)
from utils.save_to_file import save_to_file
from utils.patterns import get_population_pattern
from params import break_time, stim_time
from models.general.network import network
from plotting.connectivity_matrices import connectivity_matrices
from utils.args_config import args


class SimWrapper:
    def __init__(self, syn_params_arg=None, monitor_rate=True, monitor_state=None, report=None):
        self.net = network(syn_params_arg)
        self.report = report
        
        self.monitors = self._initialize_monitors(monitor_rate, monitor_state)
        self.net.add(self.monitors)
        
        # Store the initial state of the network so we can reset it for each run
        self.net.store('initial')

    def do_run(self, pattern, results_directory, save=True):
        # Restore the network to its pristine, t=0 state
        self.net.restore('initial')

        # Set the input pattern for this specific run
        self.net['pp'].rates = pattern['rates']

        # Run the simulation
        self._activate_monitors(False)
        self.net.run(break_time, report=self.report)
        self._activate_monitors(True)
        self.net.run(stim_time, report=self.report)

        if args.generate_graph:
            connectivity_matrices(self.net)

        if save and results_directory:
            self._save_results(pattern, results_directory)

        return (
            get_spike_monitors(self.net),
            get_rate_monitors(self.net),
            get_state_monitors(self.net),
        )

    def _initialize_monitors(self, monitor_rate, monitor_state):
        neurons = get_neurons(self.net)
        monitors = []

        spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]
        monitors.extend(spike_monitors)

        if monitor_rate:
            rate_monitors = [PopulationRateMonitor(neuron) for neuron in neurons]
            monitors.extend(rate_monitors)

        if monitor_state:
            neuron_groups_map = {ng.name: ng for ng in neurons}
            for group_name, vars_to_record in monitor_state.items():
                if group_name in neuron_groups_map:
                    neuron_group = neuron_groups_map[group_name]
                    monitors.append(StateMonitor(neuron_group, vars_to_record, record=True))
        
        return monitors

    def _activate_monitors(self, activate=True):
        for mon in self.monitors:
            mon.active = activate

    def _save_results(self, pattern, results_directory):
        mgc_pattern = get_population_pattern(get_neuron_monitor(self.net, "mgc"))
        igc_pattern = get_population_pattern(get_neuron_monitor(self.net, "igc"))
        save_to_file(results_directory, pattern, mgc_pattern, igc_pattern)
