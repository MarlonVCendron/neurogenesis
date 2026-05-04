import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
from scipy.stats import sem

from utils.data import load_pattern_data
from utils.plot_styles import cell_colors, linewidth, igc_connectivity_label
from utils.sparsity import gini_index, hoyer

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "lines.linewidth": linewidth,
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


panel_specs = [
    ('gc',   cell_colors['gc'],   'All GC', '-'),
    ('mgc',  cell_colors['mgc'],  'mGC',    '-'),
    ('igc',  cell_colors['igc'],  'iGC',    '-'),
    ('pca3', cell_colors['pca3'], 'pCA3',   '-'),
]


def _draw_panel(ax, ct, color, label, fn_means, fn_errs, ng_groups):
    ng_idx = slice(1, None)
    ctrl_val = fn_means[ct][0]
    ng_vals = np.array(fn_means[ct][ng_idx])
    ng_err  = np.array(fn_errs[ct][ng_idx])

    ctrl_line = None
    if not np.isnan(ctrl_val):
        ctrl_line, = ax.plot([], [], color=cell_colors['control'], linestyle='--')
        ax.axhline(y=ctrl_val, color=cell_colors['control'], linestyle='--')

    ax.plot(range(len(ng_groups)), ng_vals, color=color, linestyle='-')
    ax.fill_between(range(len(ng_groups)), ng_vals - ng_err, ng_vals + ng_err,
                    color=color, alpha=0.2)

    ax.set_xticks(range(len(ng_groups)))
    ax.set_xticklabels([10, '', '', 40, '', '', 70, '', '', 100])
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'.lstrip('0')))
    
    label_x = 0.9 if label == 'iGC' else 0.03 
    ax.text(label_x, 0.97, label, transform=ax.transAxes, ha='left', va='top', color=color, fontweight='bold', fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return ctrl_line


def plot_measure(fn, ylabel, outfile):
    means, errs = collect_sparsity(fn)
    ng_groups = groups[1:]

    fig, axes = plt.subplots(1, 4, figsize=(16, 4), dpi=300)

    ctrl_line = None
    for ax, (ct, color, label, _) in zip(axes, panel_specs):
        line = _draw_panel(ax, ct, color, label, means, errs, ng_groups)
        if line is not None:
            ctrl_line = line

    fig.text(0.5, 0.01, igc_connectivity_label, ha='center', va='bottom', fontsize=18)
    axes[0].set_ylabel(ylabel)

    if ctrl_line is not None:
        fig.legend([ctrl_line], ['Control'], loc='lower left', frameon=False, bbox_to_anchor=(0.1, -0.05))

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(outfile, dpi=300, format='jpg', bbox_inches='tight')
    plt.close()


plot_measure(gini_index, 'Gini Sparsity',  'figures/plots/sparsity_gini.jpg')
plot_measure(hoyer,      'Hoyer Sparsity', 'figures/plots/sparsity_hoyer.jpg')
