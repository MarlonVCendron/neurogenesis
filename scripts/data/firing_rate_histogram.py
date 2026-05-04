import numpy as np
import matplotlib.pyplot as plt

from utils.data import load_pattern_data
from utils.plot_styles import cell_colors

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16,
    "axes.titlesize": 23,
    "axes.labelsize": 22,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 20,
    "lines.linewidth": 3,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

data = load_pattern_data('rate8')
groups = sorted(list(data.keys()))

CELL_TYPES = [
    ('mgc',  'mGC'),
    ('igc',  'iGC'),
    ('pca3', 'pCA3'),
    ('ica3', 'iCA3'),
    ('hipp', 'HIPP'),
    ('bc',   'BC'),
    ('mc',   'MC'),
]


def collect_all_rates(group, exclude_single_spike=False):
    rate_lists = {ct: [] for ct, _ in CELL_TYPES}
    for trial in data[group]:
        for pattern in trial['patterns']:
            rates = pattern.get('rates', {})
            for ct, _ in CELL_TYPES:
                r = rates.get(ct, np.array([]))
                rate_lists[ct].append(r[r > 0])
    result = {}
    for ct, _ in CELL_TYPES:
        arr = np.concatenate(rate_lists[ct]) if rate_lists[ct] else np.array([])
        if exclude_single_spike and len(arr):
            arr = arr[arr > arr.min()]
        result[ct] = arr
    return result


def firing_rate_histogram(group, exclude_single_spike=False, n_bins=15, x_min=0.1, x_max=100):
    rates_dict = collect_all_rates(group, exclude_single_spike=exclude_single_spike)

    active = [(ct, label) for ct, label in CELL_TYPES if len(rates_dict[ct]) > 0]
    n = len(active)

    bins = np.logspace(np.log10(x_min), np.log10(x_max), n_bins + 1)

    fig, axes = plt.subplots(n, 1, figsize=(7, 2.2 * n), dpi=300, sharex=True)
    if n == 1:
        axes = [axes]

    for ax, (ct, label) in zip(axes, active):
        r = rates_dict[ct]
        color = cell_colors[ct]
        mean_r = np.mean(r)

        ax.hist(r, bins=bins, color=color, edgecolor='none', rwidth=0.88, zorder=2)
        ax.axvline(mean_r, color='black', linestyle='--', linewidth=1.5, zorder=3)

        ax.set_xscale('log')
        ax.set_xlim(x_min, x_max)

        for spine in ('top', 'right', 'left'):
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['bottom'].set_color('black')

        ax.set_yticks([])
        ax.tick_params(axis='x', which='both', length=0)

        ax.text(0.02, 0.85, label, transform=ax.transAxes, color=color, fontsize=18, fontweight='bold', va='top', ha='left')

        print(f'{group} | {label}: mean={mean_r:.4f} Hz, median={np.median(r):.4f} Hz, n={len(r)}')

    axes[-1].set_xlabel('Firing Rate (Hz)')
    axes[-1].set_xticks([0.1, 1, 10, 100])
    axes[-1].set_xticklabels(['0.1', '1', '10', '100'])

    plt.tight_layout(h_pad=0)

    safe_group = group.replace('.', '_')
    plt.savefig(f'figures/plots/firing_rate_histogram_{safe_group}.jpg', dpi=300, format='jpg')
    plt.close()
    print(f'Saved: figures/plots/firing_rate_histogram_{safe_group}.jpg')


ng_groups = [g for g in groups if 'neurogenesis' in g]
for group in ng_groups:
    firing_rate_histogram(group, exclude_single_spike=False)
