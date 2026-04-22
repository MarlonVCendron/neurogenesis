import numpy as np
from brian2 import *

from utils.utils import (
    get_spike_monitors,
    get_neuron_monitor,
    get_neurons,
    get_rate_monitors,
    get_state_monitors,
    neuron_ordering,
)
from utils.save_to_file import save_to_file
from utils.patterns import get_population_pattern, get_population_spike_counts
from utils.firing_rate import get_population_firing_rates
from params import break_time, stim_time
from models.general.network import network
from utils.args_config import args

TRANSITION_STEPS = 10


class SequenceSimWrapper:
    def __init__(self, monitor_rate=True, monitor_state=None, report=None, optogenetics=None):
        self.report = report
        self.optogenetics = optogenetics
        self.net = network()

        self._initialize_monitors(monitor_rate, monitor_state)
        self.net.add(self.monitors)

    def do_run(self, patterns, result_dirs):
        pp = self.net['pp']
        transition_time = args.transition_time * ms
        prev_rates = np.zeros(pp.N) * Hz

        self._activate_monitors(False)
        self.net.run(break_time, report=self.report)
        self._activate_monitors(True)

        for pattern, result_dir in zip(patterns, result_dirs):
            if transition_time > 0 * ms:
                self._run_transition(pp, prev_rates, pattern['rates'], transition_time)

            pp.rates = pattern['rates']
            t_start = self.net.t
            self._run_stim_phase()
            t_end = self.net.t
            prev_rates = pattern['rates']
            self._save_results(pattern, result_dir, t_start, t_end)

        return (
            get_spike_monitors(self.net),
            get_rate_monitors(self.net),
            get_state_monitors(self.net),
        )

    def _run_transition(self, pp, old_rates, new_rates, transition_time):
        step_duration = transition_time / TRANSITION_STEPS
        for step in range(TRANSITION_STEPS):
            alpha = (step + 1) / TRANSITION_STEPS
            pp.rates = (1 - alpha) * old_rates + alpha * new_rates
            self.net.run(step_duration, report=self.report)
        pp.rates = new_rates

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
            if group_name not in neuron_groups_map:
                continue
            neuron_group = neuron_groups_map[group_name]
            state_monitors.append(StateMonitor(neuron_group, vars_to_record, record=True))

        self.monitors += state_monitors

    def _activate_monitors(self, activate=True):
        for mon in self.monitors:
            mon.active = activate

    def _save_results(self, pattern, results_directory, t_start, t_end):
        spike_monitors = {ct: get_neuron_monitor(self.net, ct) for ct in neuron_ordering}
        save_to_file(
            results_directory=results_directory,
            pattern=pattern,
            mgc_pattern=get_population_pattern(spike_monitors['mgc'], t_start=t_start, t_end=t_end),
            igc_pattern=get_population_pattern(spike_monitors['igc'], t_start=t_start, t_end=t_end),
            pca3_pattern=get_population_pattern(spike_monitors['pca3'], t_start=t_start, t_end=t_end),
            rates={ ct: get_population_firing_rates(mon, t_start=t_start, t_end=t_end) for ct, mon in spike_monitors.items() },
            spike_counts={ ct: get_population_spike_counts(mon, t_start=t_start, t_end=t_end) for ct, mon in spike_monitors.items() },
        )

    def _run_stim_phase(self):
        if not self.optogenetics:
            self.net.run(stim_time, report=self.report)
            return

        opto = self.optogenetics
        population = self.net[opto['cell_type']]
        onset = opto['onset_time']
        duration = opto['duration']
        amount = min(opto['amount_affected'], population.N)

        self.net.run(onset, report=self.report)
        population.I_ext[:amount] = opto['current_injected']
        self.net.run(duration, report=self.report)
        population.I_ext[:amount] = 0 * amp
        self.net.run(stim_time - onset - duration, report=self.report)
