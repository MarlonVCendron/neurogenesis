import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
import h5py

RUN_NAME      = 'optogenetics'

ONSET_TIME_MS = 500.0
DURATION_MS   = 5.0
BREAK_TIME_MS = 300.0

PRE_MS        = 60.0
POST_MS       = 60.0

CELL_TYPES = [
    ('igc',  'iGC'),
    ('mgc',  'mGC'),
    ('pca3', 'pCA3'),
    ('ica3', 'iCA3'),
    ('bc',   'BC'),
    ('hipp', 'HIPP'),
    ('mc',   'MC'),
]

OUTPUT_PATH = 'figures/plots/optogenetics_spikes.jpg'

from utils.plot_styles import cell_colors

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
})


def load_data(run_name):
    base  = f'res/{run_name}'
    files = sorted(glob(f'{base}/**/*.h5', recursive=True))
    if not files:
        sys.exit(f'No .h5 files found under {base}/')

    spike_times = {}
    n_neurons   = {}

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
                    n_neurons[ct] = len(f['rates'][ct])

    return spike_times, n_neurons


def main():
    onset_abs = BREAK_TIME_MS + ONSET_TIME_MS

    spike_times, n_neurons = load_data(RUN_NAME)

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

        ax.axvspan(0, DURATION_MS, color='cyan', alpha=0.15, zorder=0)
        ax.axvline(0, color='cyan', linewidth=0.8, zorder=1)
        ax.axvline(DURATION_MS, color='cyan', linewidth=0.8, zorder=1)
        ax.plot([0, DURATION_MS], [n_neur, n_neur], color='cyan', linewidth=0.8, zorder=1, clip_on=False)
        ax.plot([-PRE_MS, 0], [0, 0], color='cyan', linewidth=0.8, zorder=2, clip_on=False)
        ax.plot([DURATION_MS, POST_MS], [0, 0], color='cyan', linewidth=0.8, zorder=2, clip_on=False)

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

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight', format='jpg')
    plt.close()
    print(f'Saved: {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
