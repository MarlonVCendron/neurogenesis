import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.stats import sem

from utils.data import load_pattern_data
from utils.plot_styles import cell_colors
from utils.sparsity import gini_index, hoyer

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "lines.linewidth": 6,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

data = load_pattern_data('april_2026')
groups = sorted(list(data.keys()))


def compute_sparsity(spike_counts, fn, has_neurogenesis):
    """Compute sparsity for each cell type and the combined gc population."""
    mgc = spike_counts.get('mgc', np.array([]))
    igc = spike_counts.get('igc', np.array([]))
    pca3 = spike_counts.get('pca3', np.array([]))

    gc = np.concatenate([mgc, igc]) if has_neurogenesis and len(igc) > 0 else mgc

    return {
        'mgc': fn(mgc) if len(mgc) > 0 else np.nan,
        'igc': fn(igc) if has_neurogenesis and len(igc) > 0 else np.nan,
        'pca3': fn(pca3) if len(pca3) > 0 else np.nan,
        'gc': fn(gc) if len(gc) > 0 else np.nan,
    }


def collect_sparsity(fn):
    """Collect mean sparsity and SEM per group for each cell type."""
    group_values = {g: {'mgc': [], 'igc': [], 'pca3': [], 'gc': []} for g in groups}

    for group in groups:
        has_neurogenesis = 'neurogenesis' in group
        for trial in data[group]:
            for pattern in trial['patterns'][:-1]:
                sc = pattern.get('spike_counts', {})
                if not sc:
                    continue
                vals = compute_sparsity(sc, fn, has_neurogenesis)
                for ct in vals:
                    if not np.isnan(vals[ct]):
                        group_values[group][ct].append(vals[ct])

    means = {ct: [] for ct in ['mgc', 'igc', 'pca3', 'gc']}
    errors = {ct: [] for ct in ['mgc', 'igc', 'pca3', 'gc']}

    for group in groups:
        for ct in means:
            vals = group_values[group][ct]
            means[ct].append(np.mean(vals) if vals else np.nan)
            errors[ct].append(sem(vals) if len(vals) > 1 else 0.0)

    return means, errors


def plot_sparsity():
    gini_means, gini_errs = collect_sparsity(gini_index)
    hoyer_means, hoyer_errs = collect_sparsity(hoyer)

    ng_groups = groups[1:]
    ng_idx = slice(1, None)

    fig, axes = plt.subplots(1, 2, figsize=(20, 10), dpi=300)

    population_specs = [
        ('gc',   cell_colors['gc'],   'Full GC (mGC+iGC)', '-'),
        ('mgc',  cell_colors['mgc'],  'mGC',               '--'),
        ('igc',  cell_colors['igc'],  'iGC',               '--'),
        ('pca3', cell_colors['pca3'], 'pCA3',              '-'),
    ]

    for ax, (fn_means, fn_errs, title, ylabel) in zip(axes, [
        (gini_means, gini_errs, 'Gini Index', 'Gini Sparsity'),
        (hoyer_means, hoyer_errs, 'Hoyer Measure', 'Hoyer Sparsity'),
    ]):
        ax.set_title(title)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=10))

        for ct, color, label, ls in population_specs:
            ctrl_val = fn_means[ct][0]
            ng_vals = np.array(fn_means[ct][ng_idx])
            ng_err  = np.array(fn_errs[ct][ng_idx])

            # Skip if no data at all for this cell type
            if np.all(np.isnan(ng_vals)):
                continue

            # Control dashed line only for gc (full population baseline)
            if ct == 'gc' and not np.isnan(ctrl_val):
                ax.axhline(y=ctrl_val, color=cell_colors['control'], linestyle='--', label='Control (GC)')

            ax.plot(range(len(ng_groups)), ng_vals, color=color, label=label, marker='', linestyle=ls)
            ax.fill_between(range(len(ng_groups)), ng_vals - ng_err, ng_vals + ng_err, color=color, alpha=0.2)

        xlabels = range(10, 10 * len(ng_groups) + 1, 10)
        ax.set_xticks(range(len(ng_groups)))
        ax.set_xticklabels(xlabels)
        ax.set_xlabel('Connectivity (%)')
        ax.set_ylabel(ylabel)
        ax.legend(frameon=False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    plt.tight_layout()
    plt.savefig('figures/plots/sparsity.jpg', dpi=300, format='jpg', bbox_inches='tight')
    plt.close()


plot_sparsity()
