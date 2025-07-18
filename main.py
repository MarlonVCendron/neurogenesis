import tqdm_pathos
from os.path import join

from plotting.spikes_and_rates import plot_spikes_and_rates
from plotting.state_monitors import plot_state_monitors
from utils.patterns import generate_activity_patterns
from utils.initialize import initialize
from sim import SimWrapper
from params import results_dir, trials, igc_conn, has_ca3, has_igc
from utils.args_config import args


def res_filename(i, total):
    patterns_per_trial = total // trials
    trial_index = i // patterns_per_trial
    pattern_index = i % patterns_per_trial
    flag = f"neurogenesis_{igc_conn}" if has_igc else "control"
    flag += "_ca3" if has_ca3 else ""
    return f"{args.prefix}/{flag}_trial_{trial_index}_pattern_{pattern_index}"


if __name__ == "__main__":
    initialize()

    monitor_rate = args.single_run
    report = "text" if args.single_run else None
    # monitor_state = {"hipp": ["I_syn_1", "I_syn_2", "I_syn_3", "I_syn_4", "I_syn_5", "I", "U", "Vm"]}
    monitor_state = None
    sim = SimWrapper(report=report, monitor_rate=monitor_rate, monitor_state=monitor_state)

    patterns = [pattern for _ in range(trials) for pattern in generate_activity_patterns()]
    if args.single_run:
        patterns = patterns[:1]

    total_patterns = len(patterns)
    result_dirs = [
        join(results_dir, res_filename(i, total_patterns)) for i in range(total_patterns)
    ]

    results = tqdm_pathos.starmap(sim.do_run, zip(patterns, result_dirs))

    if monitor_rate:
        for i, (spikes, rates, states) in enumerate(results):
            plot_state_monitors(states, filename=res_filename(i, total_patterns))
            plot_spikes_and_rates(spikes, rates, i, filename=res_filename(i, total_patterns))
