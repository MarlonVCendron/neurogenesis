import tqdm_pathos
from os.path import join
from brian2 import nA, ms

from plotting.spikes_and_rates import plot_spikes_and_rates
from plotting.state_monitors import plot_state_monitors
from utils.patterns import generate_activity_patterns
from utils.initialize import initialize
from sim import SimWrapper, SequenceSimWrapper
from params import results_dir, trials, igc_conn, has_ca3, has_igc, break_time, stim_time
from utils.args_config import args


def res_filename(i, total):
    patterns_per_trial = total // trials
    trial_index = i // patterns_per_trial
    pattern_index = i % patterns_per_trial
    flag = f"neurogenesis_{igc_conn}" if has_igc else "control"
    flag += "_ca3" if has_ca3 else ""
    return f"{args.prefix}/{flag}_trial_{trial_index}_pattern_{pattern_index}"

def optogenetics():
    if not args.optogenetics:
        return
    return {
        "cell_type": 'igc',
        "amount_affected": 50,
        "current_injected": 0.5 * nA,
        # "current_injected": 0 * nA,
        "onset_time": 500 * ms,
        "duration": 5 * ms,
    }


if __name__ == "__main__":
    initialize()

    monitor_rate = args.single_run or not args.skip_rates
    report = "text" if args.single_run else None
    # monitor_state = {"hipp": ["I_syn_1", "I_syn_2", "I_syn_3", "I_syn_4", "I_syn_5", "I", "U", "Vm"]}
    monitor_state = None

    patterns = [pattern for _ in range(trials) for pattern in generate_activity_patterns()]
    if args.single_run and not args.pattern_sequence_mode:
        patterns = patterns[:1]

    total_patterns = len(patterns)
    result_dirs = [
        join(results_dir, res_filename(i, total_patterns)) for i in range(total_patterns)
    ]

    if args.pattern_sequence_mode:
        patterns_per_trial = total_patterns // trials
        for trial_idx in range(trials):
            start = trial_idx * patterns_per_trial
            trial_patterns = patterns[start : start + patterns_per_trial]
            trial_result_dirs = result_dirs[start : start + patterns_per_trial]

            seq_sim = SequenceSimWrapper(
                report=report,
                monitor_rate=monitor_rate,
                monitor_state=monitor_state,
                optogenetics=optogenetics(),
            )
            spikes, rates, states = seq_sim.do_run(trial_patterns, trial_result_dirs)

            if args.single_run:
                t_end_seq = break_time + len(trial_patterns) * stim_time
                plot_spikes_and_rates(
                    spikes, rates,
                    filename=res_filename(start, total_patterns),
                    t_end=t_end_seq,
                )
    else:
        sim = SimWrapper(
            report=report,
            monitor_rate=monitor_rate,
            monitor_state=monitor_state,
            optogenetics=optogenetics()
        )

        results = tqdm_pathos.starmap(sim.do_run, zip(patterns, result_dirs))

        if args.single_run:
            for i, (spikes, rates, states) in enumerate(results):
                plot_state_monitors(states, filename=res_filename(i, total_patterns))
                plot_spikes_and_rates(spikes, rates, i, filename=res_filename(i, total_patterns))
