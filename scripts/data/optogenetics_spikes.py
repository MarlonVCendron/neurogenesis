import os
import re
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
import h5py
from utils.plot_styles import cell_colors
from utils.args_config import args

NEG = False
ALL_LEVELS = False # Joins all the runs into one plot

# RUN_NAME = 'final_opto_negative' if NEG else 'final_opto_positive'
RUN_NAME = 'FINAL_opto_june_positive'

ONSET_TIME_MS = 400
DURATION_MS   = 30.0 if NEG else 5.0
BREAK_TIME_MS = 300.0

PRE_MS  = 25 if NEG else 60
POST_MS = 95 if NEG else 60

CELL_TYPES = [
    ('igc',  'iGC'),
    ('mgc',  'mGC'),
    ('mc',   'MC'),
    ('bc',   'BC'),
    ('hipp', 'HIPP'),
    ('pca3', 'pCA3'),
    ('ica3', 'iCA3'),
]

opto_color = 'red' if NEG else 'lime'

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
})


def load_data(group_file_path):
    files = sorted(glob(f'{group_file_path}*/**/*.h5', recursive=True))
    # files = sorted(glob(f'{base}/neurogenesis_0.5_ca3_trial_0_pattern_0/*.h5', recursive=True))
    # files = sorted(glob(f'{base}/neurogenesis_0.4_ca3_trial_0_pattern_0/*.h5', recursive=True))
    # files = sorted(glob(f'{base}/neurogenesis_0.1_ca3_trial_*/*.h5', recursive=True))
    if not files:
        sys.exit(f'No .h5 files found under {base}/')

    spike_times = {}
    n_neurons   = {'bc': args.n_bc, 'hipp': args.n_hipp, 'ica3': args.n_ica3, 'igc': args.n_igc, 'mc': args.n_mc, 'mgc': args.n_mgc - args.n_igc, 'pca3': args.n_pca3, 'pp': args.n_pp}

    # Take only first file or all
    files = files if ALL_LEVELS else files[:1]
    for fpath in files:
        with h5py.File(fpath, 'r') as f:
            if 'spike_times' not in f:
                sys.exit(
                    f'File {fpath} has no spike_times group.\n'
                    'Re-run the simulation with --optogenetics using the updated code.'
                )
            for ct in f['spike_times'].keys():
                t = np.array(f['spike_times'][ct]['times_ms'], dtype=np.float64)
                i = np.array(f['spike_times'][ct]['indices'],  dtype=np.int32)
                spike_times.setdefault(ct, []).append((t, i))
                if ct not in n_neurons and 'rates' in f and ct in f['rates']:
                    if len(f['rates'][ct]):
                        n_neurons[ct] = len(f['rates'][ct])

    return spike_times, n_neurons


def main(group_file_path):
    onset_abs = BREAK_TIME_MS + ONSET_TIME_MS

    spike_times, n_neurons = load_data(group_file_path)

    active = [(ct, lbl) for ct, lbl in CELL_TYPES if ct in spike_times]

    n_panels = len(active)
    fig, axes = plt.subplots(
        n_panels, 1,
        figsize=(6, 1.8 * n_panels),
        dpi=300,
        sharex=True,
    )
    if n_panels == 1:
        axes = [axes]

    t_start = onset_abs - PRE_MS
    t_end   = onset_abs + POST_MS

    for ax, (ct, label) in zip(axes, active):
        color  = cell_colors.get(ct, '#333333')
        n_neur = n_neurons.get(ct, 1)

        all_t = []
        all_i = []
        for times, indices in spike_times[ct]:
            mask = (times >= t_start) & (times <= t_end)
            all_t.append(times[mask] - onset_abs)
            all_i.append(indices[mask])

        rel_t = np.concatenate(all_t) if all_t else np.array([])
        idx   = np.concatenate(all_i) if all_i else np.array([])

        ax.plot(rel_t, idx, 'ok', markersize=1)

        ax.axvspan(0, DURATION_MS, color=opto_color, alpha=0.15, zorder=0)
        ax.axvline(0, color=opto_color, linewidth=0.8, zorder=1)
        ax.axvline(DURATION_MS, color=opto_color, linewidth=0.8, zorder=1)
        ax.plot([0, DURATION_MS], [n_neur, n_neur], color=opto_color, linewidth=0.8, zorder=1, clip_on=False)
        ax.plot([-PRE_MS, 0], [0, 0], color=opto_color, linewidth=0.8, zorder=2, clip_on=False)
        ax.plot([DURATION_MS, POST_MS], [0, 0], color=opto_color, linewidth=0.8, zorder=2, clip_on=False)

        ax.set_ylim(0, n_neur)
        ax.set_yticks([0, n_neur])

        ax.set_ylabel(label, color=color, fontsize=16, fontweight='bold', rotation=0, ha='left', va='top')
        ax.yaxis.set_label_coords(0.04, 1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='both', length=0)

    axes[-1].set_xlabel('Time with respect to iGC current injection (ms)')
    axes[-1].set_xlim(-PRE_MS, POST_MS)

    fig.text(0.05, 0.5, 'Neuron index', va='center', ha='left', rotation='vertical', fontsize=18)

    plt.tight_layout(rect=[0.06, 0, 1, 1], h_pad=0.4)

    sign = 'neg' if NEG else 'pos'
    p = re.compile(r".*(\d.\d)")
    neurogenesis_level = 'all' if ALL_LEVELS else p.search(group_file_path).group(1)
    output_path = f'figures/plots/optogenetics/spikes_{sign}_{neurogenesis_level}.jpg'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', format='jpg')
    plt.close()
    print(f'Saved: {output_path}')


if __name__ == '__main__':
    base  = f'res/{RUN_NAME}'
    files = sorted(glob(f'{base}/*'))

    groups_file_paths = set([])
    if ALL_LEVELS:
        groups_file_paths = set([base])
    else:
        groups_file_paths = set([file.split('_ca3')[0] for file in files])

    for group_file_path in groups_file_paths:
        main(group_file_path)
