from brian2 import *
from brian2.codegen.codeobject import CodeObject
from brian2.core.functions import DEFAULT_FUNCTIONS

def _patched_codeobject_getstate(self):
    state = self.__dict__.copy()
    state["owner"] = self.owner.__repr__.__self__
    state["variables"] = self.variables.copy()
    for k, v in state["variables"].items():
        if isinstance(v, Function) and k in DEFAULT_FUNCTIONS and v is DEFAULT_FUNCTIONS[k]:
            state["variables"][k] = k
    return state

CodeObject.__getstate__ = _patched_codeobject_getstate

from utils.utils import (
    get_spike_monitors,
    get_neuron_monitor,
    get_neurons,
    get_rate_monitors,
    get_state_monitors,
    neuron_ordering,
)
from utils.save_to_file import save_to_file
from utils.patterns import get_population_pattern, get_population_spike_counts, get_spike_times
from utils.firing_rate import get_population_firing_rates
from params import break_time, stim_time
from models.general.network import network
from plotting.connectivity_matrices import connectivity_matrices
from utils.args_config import args


class SimWrapper:
    def __init__(self, monitor_rate=True, monitor_state=None, report=None, optogenetics=None):
        self.optogenetics = optogenetics
        self.net = network()

        self._initialize_monitors(monitor_rate, monitor_state)
        self.net.add(self.monitors)

        self._activate_monitors(False)
        self.net.run(break_time, report=report)
        self._activate_monitors(True)
        self._run_stim_phase(report)

        device.build(run=False)
        self.device = get_device()

    def do_run(self, pattern, results_directory):
        from brian2.devices import device_module

        device_module.active_device = self.device

        self.device.run(run_args={
            self.net["pp"].rates: pattern["rates"],
        })

        if args.generate_graph:
            connectivity_matrices(self.net)

        self._save_results(pattern, results_directory)

        return (
            get_spike_monitors(self.net),
            get_rate_monitors(self.net),
            get_state_monitors(self.net),
        )

    def _initialize_monitors(self, monitor_rate, monitor_state):
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

    def _activate_monitors(self, activate=True):
        for mon in self.monitors:
            mon.active = activate

    def _save_results(self, pattern, results_directory):
        spike_monitors = {ct: get_neuron_monitor(self.net, ct) for ct in neuron_ordering}
        save_to_file(
            results_directory=results_directory,
            pattern=pattern,
            mgc_pattern=get_population_pattern(spike_monitors["mgc"]),
            igc_pattern=get_population_pattern(spike_monitors["igc"]),
            pca3_pattern=get_population_pattern(spike_monitors["pca3"]),
            rates={ct: get_population_firing_rates(mon) for ct, mon in spike_monitors.items()},
            spike_counts={ct: get_population_spike_counts(mon) for ct, mon in spike_monitors.items()},
            spike_times={ct: get_spike_times(mon) for ct, mon in spike_monitors.items()},
        )

    def _run_stim_phase(self, report):
        if not self.optogenetics:
            self.net.run(stim_time, report=report)
            return

        opto = self.optogenetics
        population = self.net[opto["cell_type"]]
        onset = opto["onset_time"]
        duration = opto["duration"]
        amount = min(opto["amount_affected"], population.N)

        self.net.run(onset, report=report)
        population.I_ext[:amount] = opto["current_injected"]
        self.net.run(duration, report=report)
        population.I_ext[:amount] = 0 * amp
        self.net.run(stim_time - onset - duration, report=report)
