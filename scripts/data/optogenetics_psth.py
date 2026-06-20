import os
import math
import re
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
import h5py

NEG = False
ALL_LEVELS = True  # Joins all the runs into one plot

# RUN_NAME = 'final_opto_negative' if NEG else 'final_opto_positive'
# RUN_NAME = 'FINAL_opto_june_positive'
# RUN_NAME = 'weak_opto_june_positive'
RUN_NAME = 'opto_correct_june_positive'

ONSET_TIME_MS = 400
DURATION_MS   = 30.0 if NEG else 5.0
BREAK_TIME_MS = 300.0

PRE_MS        = 25 if NEG else 60
POST_MS       = 95 if NEG else 60

BIN_SIZE_MS   = 1.5

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

from utils.plot_styles import cell_colors

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})


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


def compute_psth_zscore(trials, n_neurons, onset_abs):
    plot_start = onset_abs - PRE_MS
    plot_end   = onset_abs + POST_MS

    bins        = np.arange(plot_start, plot_end + BIN_SIZE_MS, BIN_SIZE_MS)
    before_bins = np.arange(BREAK_TIME_MS, plot_start + BIN_SIZE_MS, BIN_SIZE_MS)

    bin_centers = (bins[:-1] + bins[1:]) / 2.0 - onset_abs

    psth_counts   = np.zeros(len(bins) - 1)
    before_counts = np.zeros(max(len(before_bins) - 1, 1))
    n_trials = len(trials)

    for times, _ in trials:
        psth_counts += np.histogram(times, bins=bins)[0]
        if len(before_bins) > 1:
            before_counts += np.histogram(times, bins=before_bins)[0]

    scale       = n_neurons * n_trials * (BIN_SIZE_MS / 1000.0)
    psth_rate   = psth_counts   / scale
    before_rate = before_counts / scale

    bl_mean = np.mean(before_rate)
    bl_std  = np.std(before_rate) if np.std(before_rate) > 1e-10 else 1.0

    return bin_centers, (psth_rate - bl_mean) / bl_std


def draw_stimulus_indicator(ax, ymax, ymin):
    y_flat = ymin - (abs(ymax) * 0.05)

    xs = [-PRE_MS, 0,      0,    DURATION_MS, DURATION_MS, POST_MS]
    ys = [y_flat,  y_flat, ymax,  ymax,         y_flat,      y_flat]
    ax.plot(xs, ys, color=opto_color, lw=1.2, solid_joinstyle='miter', solid_capstyle='butt', clip_on=False, zorder=5)
    ax.axvspan(0, DURATION_MS, color=opto_color, alpha=0.15, zorder=0)
    return abs(y_flat)


def main(group_file_path):
    onset_abs = BREAK_TIME_MS + ONSET_TIME_MS

    spike_times, n_neurons = load_data(group_file_path)

    active = [(neuron, label) for neuron, label in CELL_TYPES if neuron in spike_times]

    n_panels = len(active)
    fig, axes = plt.subplots(
        n_panels, 1,
        figsize=(6, 1.5 * n_panels),
        dpi=300,
        sharex=True,
    )
    if n_panels == 1:
        axes = [axes]

    for ax, (neuron, label) in zip(axes, active):
        color  = cell_colors.get(neuron, '#333333')
        n_neur = n_neurons.get(neuron, 1)

        bin_centers, zscore = compute_psth_zscore(spike_times[neuron], n_neur, onset_abs)

        ax.bar(bin_centers, zscore, width=BIN_SIZE_MS * 0.85, color='black', align='center', zorder=2)
        ax.axhline(0, color='black', linewidth=0.6, zorder=1)

        zmax = max(float(zscore.max()) * 1.15, 1.0)
        zmin = float(zscore.min())
        indicator_h = draw_stimulus_indicator(ax, zmax, zmin)
        if not math.isnan(indicator_h) and not math.isnan(zmax):
            ax.set_ylim(-indicator_h, zmax)

        ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=2, min_n_ticks=3, steps=[1, 2, 5, 10], integer=True))

        ax.set_ylabel(label, color=color, fontsize=16, fontweight='bold', rotation=0, ha='left', va='top')
        ax.yaxis.set_label_coords(0.04, 1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='both', length=0)

    axes[-1].set_xlabel('Time with respect to iGC current injection (ms)')
    axes[-1].set_xlim(-PRE_MS, POST_MS)

    fig.text(0.05, 0.5, 'Change in firing rate (Z-score)', va='center', ha='left', rotation='vertical', fontsize=18)

    plt.tight_layout(rect=[0.06, 0, 1, 1], h_pad=0.4)

    sign = 'neg' if NEG else 'pos'
    p = re.compile(r".*(\d.\d)")
    neurogenesis_level = 'all' if ALL_LEVELS else p.search(group_file_path).group(1)
    output_path = f'figures/plots/optogenetics/{RUN_NAME}/psth_{sign}_{neurogenesis_level}.jpg'
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
