import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
import h5py

RUN_NAME        = 'optogenetics'

ONSET_TIME_MS   = 500.0
DURATION_MS     = 5.0
BREAK_TIME_MS   = 300.0

PRE_MS          = 60.0
POST_MS         = 60.0

BIN_SIZE_MS     = 2.0

CELL_TYPES = [
    ('igc',  'iGC'),
    ('mgc',  'mGC'),
    ('pca3', 'pCA3'),
    ('ica3', 'iCA3'),
    ('bc',   'BC'),
    ('hipp', 'HIPP'),
    ('mc',   'MC'),
]

OUTPUT_PATH = 'figures/plots/optogenetics_psth.jpg'

from utils.plot_styles import cell_colors

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
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


def compute_psth_zscore(trials, n_neurons, onset_abs):
    plot_start = onset_abs - PRE_MS
    plot_end   = onset_abs + POST_MS

    bins     = np.arange(plot_start, plot_end + BIN_SIZE_MS, BIN_SIZE_MS)
    bl_bins  = np.arange(BREAK_TIME_MS, plot_start + BIN_SIZE_MS, BIN_SIZE_MS)

    bin_centers = (bins[:-1] + bins[1:]) / 2.0 - onset_abs

    psth_counts = np.zeros(len(bins) - 1)
    bl_counts   = np.zeros(max(len(bl_bins) - 1, 1))
    n_trials    = len(trials)

    for times, _ in trials:
        psth_counts += np.histogram(times, bins=bins)[0]
        if len(bl_bins) > 1:
            bl_counts += np.histogram(times, bins=bl_bins)[0]

    scale      = n_neurons * n_trials * (BIN_SIZE_MS / 1000.0)
    psth_rate  = psth_counts / scale
    bl_rate    = bl_counts   / scale

    bl_mean = np.mean(bl_rate)
    bl_std  = np.std(bl_rate) if np.std(bl_rate) > 1e-10 else 1.0

    return bin_centers, (psth_rate - bl_mean) / bl_std


def draw_stimulus_indicator(ax, ymax, ymin):
    y_flat = ymin - (abs(ymax) * 0.05)

    xs = [-PRE_MS, 0,      0,    DURATION_MS, DURATION_MS, POST_MS]
    ys = [y_flat,  y_flat, ymax,  ymax,         y_flat,      y_flat]
    ax.plot(xs, ys, color='cyan', lw=1.2, solid_joinstyle='miter', solid_capstyle='butt', clip_on=False, zorder=5)
    return abs(y_flat)


def main():
    onset_abs = BREAK_TIME_MS + ONSET_TIME_MS

    spike_times, n_neurons = load_data(RUN_NAME)

    active = [(ct, lbl) for ct, lbl in CELL_TYPES if ct in spike_times]

    n_panels = len(active)
    fig, axes = plt.subplots(
        n_panels, 1,
        figsize=(6, 1.5 * n_panels),
        dpi=300,
        sharex=True,
    )
    if n_panels == 1:
        axes = [axes]

    for ax, (ct, label) in zip(axes, active):
        color  = cell_colors.get(ct, '#333333')
        n_neur = n_neurons.get(ct, 1)

        bin_centers, zscore = compute_psth_zscore(
            spike_times[ct], n_neur, onset_abs,
        )

        ax.bar(bin_centers, zscore, width=BIN_SIZE_MS * 0.85,
               color='black', align='center', zorder=2)
        ax.axhline(0, color='black', linewidth=0.6, zorder=1)

        zmax = max(float(zscore.max()) * 1.15, 1.0)
        zmin = float(zscore.min()) 
        indicator_h = draw_stimulus_indicator(ax, zmax, zmin)
        ax.set_ylim(-indicator_h, zmax)

        ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=2, min_n_ticks=3, steps=[1, 2, 5, 10], integer=True))

        ax.set_ylabel(label, color=color, fontsize=16, fontweight='bold', rotation=0, ha='left', va='top')
        ax.yaxis.set_label_coords(0.04, 1)


        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    axes[-1].set_xlabel('Time with respect to iGC current injection (ms)')
    axes[-1].set_xlim(-PRE_MS, POST_MS)

    fig.text(0.05, 0.5, 'Change in firing rate (Z-score)', va='center', ha='left', rotation='vertical', fontsize=18)

    plt.tight_layout(rect=[0.06, 0, 1, 1], h_pad=0.4)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight', format='jpg')
    plt.close()
    print(f'Saved: {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
