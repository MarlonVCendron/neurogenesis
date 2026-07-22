import sys
import numpy as np
from glob import glob
import h5py

RUN_NAME      = 'opto_final_july_positive'
ONSET_TIME_MS = 400
BREAK_TIME_MS = 300.0
PRE_MS        = 60    # baseline ends this many ms before the pulse (matches PSTH baseline)
POST_MS       = 60    # window after activation (ms); matches ±60ms PSTH display window
BIN_SIZE_MS   = 1.5
Z_THRESHOLD   = 1.96  # ~p < 0.05 two-tailed

CELL_TYPES = [
    ('igc',  'iGC'),
    ('mgc',  'mGC'),
    ('mc',   'MC'),
    ('bc',   'BC'),
    ('hipp', 'HIPP'),
    ('pca3', 'pCA3'),
    ('ica3', 'iCA3'),
]


def load_data(group_file_path):
    files = sorted(glob(f'{group_file_path}*/**/*.h5', recursive=True))
    if not files:
        sys.exit(f'No .h5 files found under {group_file_path}/')

    spike_times = {}
    n_neurons   = {}

    for fpath in files:
        with h5py.File(fpath, 'r') as f:
            for neuron in f['spike_times'].keys():
                times   = np.array(f['spike_times'][neuron]['times_ms'], dtype=np.float64)
                indices = np.array(f['spike_times'][neuron]['indices'],  dtype=np.int32)
                spike_times.setdefault(neuron, []).append((times, indices))
                if neuron not in n_neurons:
                    n_neurons[neuron] = len(f['rates'][neuron])
                n_neurons[neuron] = max(len(f['rates'][neuron]), n_neurons[neuron])

    return spike_times, n_neurons


def compute_mean_zscore(trials, n_neurons, onset_abs):
    baseline_bins = np.arange(BREAK_TIME_MS, onset_abs - PRE_MS + BIN_SIZE_MS, BIN_SIZE_MS)
    post_bins     = np.arange(onset_abs, onset_abs + POST_MS + BIN_SIZE_MS, BIN_SIZE_MS)

    n_trials = len(trials)
    scale    = n_neurons * n_trials * (BIN_SIZE_MS / 1000.0)

    baseline_counts = np.zeros(len(baseline_bins) - 1)
    post_counts     = np.zeros(len(post_bins) - 1)

    for times, _ in trials:
        baseline_counts += np.histogram(times, bins=baseline_bins)[0]
        post_counts     += np.histogram(times, bins=post_bins)[0]

    baseline_rate = baseline_counts / scale
    post_rate     = post_counts     / scale

    bl_mean = np.mean(baseline_rate)
    bl_std  = np.std(baseline_rate) if np.std(baseline_rate) > 1e-10 else 1.0

    post_zscore = (post_rate - bl_mean) / bl_std
    return np.mean(post_zscore)


def main(group_file_path):
    onset_abs = BREAK_TIME_MS + ONSET_TIME_MS  # 700 ms

    spike_times, n_neurons = load_data(group_file_path)

    print(f'\nResults for: {group_file_path}')
    print(f'{"Population":<12} {"Mean Z-score":>13} {"Effect":>10}')
    print('-' * 38)

    for neuron, label in CELL_TYPES:
        if neuron not in spike_times:
            continue

        z = compute_mean_zscore(spike_times[neuron], n_neurons[neuron], onset_abs)

        if z > Z_THRESHOLD:
            effect = 'INCREASE'
        elif z < -Z_THRESHOLD:
            effect = 'DECREASE'
        else:
            effect = 'NO CHANGE'

        print(f'{label:<12} {z:>13.2f} {effect:>10}')


if __name__ == '__main__':
    base  = f'res/{RUN_NAME}'
    files = sorted(glob(f'{base}/*'))

    groups = set(f.split('_ca3')[0] for f in files)

    for group_file_path in sorted(groups):
        main(group_file_path)
