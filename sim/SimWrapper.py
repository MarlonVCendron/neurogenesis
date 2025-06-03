from brian2 import *

from utils.utils import (
    get_spike_monitors,
    get_neuron_monitor,
    get_neurons,
    get_rate_monitors,
    get_state_monitors,
)
from utils.save_to_file import save_to_file
from utils.patterns import get_population_pattern
from params import break_time, stim_time
from models.general.network import network
from plotting.connectivity_matrices import connectivity_matrices
from utils.args_config import args


class SimWrapper:
    def __init__(self, monitor_rate=True, monitor_state=None, report=None):
        self.net = network()

        self.initialize_monitors(monitor_rate, monitor_state)
        self.net.add(self.monitors)

        self.activate_monitors(False)
        self.net.run(break_time, report=report)
        self.activate_monitors(True)
        self.net.run(stim_time, report=report)

        device.build(run=False)
        self.device = get_device()

    def do_run(self, pattern, results_directory):
        from brian2.devices import device_module

        device_module.active_device = self.device

        self.device.run(run_args={self.net["pp"].rates: pattern["rates"]})

        if args.generate_graph:
            connectivity_matrices(self.net)

        self.save_results(pattern, results_directory)

        return (
            get_spike_monitors(self.net),
            get_rate_monitors(self.net),
            get_state_monitors(self.net),
        )

    def initialize_monitors(self, monitor_rate, monitor_state):
        neurons = get_neurons(self.net)

        spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]
        rate_monitors = (
            [PopulationRateMonitor(neuron) for neuron in neurons] if monitor_rate else []
        )

        self.monitors = spike_monitors + rate_monitors

        if not monitor_state:
            return

        state_monitors = []
        neuron_groups_map = {ng.name: ng for ng in neurons}
        for group_name, vars_to_record in monitor_state.items():
            if not group_name in neuron_groups_map:
                continue
            neuron_group = neuron_groups_map[group_name]
            state_monitors.append(StateMonitor(neuron_group, vars_to_record, record=True))

        self.monitors += state_monitors

    def activate_monitors(self, activate=True):
        for mon in self.monitors:
            mon.active = activate

    def save_results(self, pattern, results_directory):
        mgc_pattern = get_population_pattern(get_neuron_monitor(self.net, "mgc"))
        igc_pattern = get_population_pattern(get_neuron_monitor(self.net, "igc"))
        save_to_file(results_directory, pattern, mgc_pattern, igc_pattern)
