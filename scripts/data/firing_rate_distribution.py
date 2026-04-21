import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, mode

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

data = load_pattern_data('rate5')
groups = sorted(list(data.keys()))


def collect_rates(group, exclude_single_spike=False):
    """Return concatenated firing rates (>0) for mgc and igc across all trials/patterns."""
    mgc_rates, igc_rates = [], []
    for trial in data[group]:
        for pattern in trial['patterns']:
            rates = pattern.get('rates', {})
            mgc_r = rates.get('mgc', np.array([]))
            igc_r = rates.get('igc', np.array([]))
            mgc_rates.append(mgc_r[mgc_r > 0])
            igc_rates.append(igc_r[igc_r > 0])
    mgc = np.concatenate(mgc_rates)
    igc = np.concatenate(igc_rates)
    if exclude_single_spike:
        # cells that fired exactly once all share the same rate (1/duration = min rate)
        if len(mgc): mgc = mgc[mgc > mgc.min()]
        if len(igc): igc = igc[igc > igc.min()]
    return mgc, igc


def plot_kde(ax, rates, color, label, bw=0.25, show_mean=True):
    """Plot a normalized KDE on a log x-axis with filled area and white outline."""
    rates = np.asarray(rates)
    rates = rates[rates > 0]
    if len(rates) == 0:
        return
    log_r = np.log10(rates)
    kde = gaussian_kde(log_r, bw_method=bw)
    x_log = np.linspace(log_r.min() - 0.3, log_r.max() + 0.3, 1000)
    y = kde(x_log)
    y = y / y.max()
    x = 10 ** x_log
    ax.fill_between(x, y, alpha=0.6, color=color, label=label)
    ax.plot(x, y, color='white', linewidth=2.5, solid_joinstyle='round', solid_capstyle='round')

    mean_rate = np.mean(rates)
    if show_mean:
        ax.axvline(mean_rate, color=color, linestyle='--', linewidth=2, alpha=0.9)
        y_at_mean = kde(np.log10(mean_rate)) / kde(x_log).max()
        ax.text(
            mean_rate, float(y_at_mean) + 0.06,
            f'{mean_rate:.2f} Hz',
            color=color, fontsize=12, ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7),
        )
    return mean_rate


def firing_rate_distribution(show_mean=True, exclude_single_spike=False):
    ng_groups = [g for g in groups if 'neurogenesis' in g]

    ncols = len(ng_groups)
    fig, axes = plt.subplots(1, ncols, figsize=(8 * ncols, 8), dpi=300, sharey=True)
    if ncols == 1:
        axes = [axes]

    for ax, group in zip(axes, ng_groups):
        mgc_rates, igc_rates = collect_rates(group, exclude_single_spike=exclude_single_spike)

        mgc_mean = plot_kde(ax, mgc_rates, color=cell_colors['mgc'], label='mGC', bw=0.5, show_mean=show_mean)
        igc_mean = plot_kde(ax, igc_rates, color=cell_colors['igc'], label='iGC', bw=0.5, show_mean=show_mean)

        print(f'{group} summary:')
        print(f'mgc mean: {mgc_mean:.4f} Hz, mode: {mode(mgc_rates).mode} ({mode(mgc_rates).count}), median: {np.median(mgc_rates):.4f} Hz, std: {np.std(mgc_rates):.4f}')
        print(f'igc mean: {igc_mean:.4f} Hz, mode: {mode(igc_rates).mode} ({mode(igc_rates).count}), median: {np.median(igc_rates):.4f} Hz, std: {np.std(igc_rates):.4f}')

        # group format: 'neurogenesis_0.2' or 'neurogenesis_0.2_ca3' etc.
        parts = group.split('_')
        connectivity = next(p for p in parts if p.replace('.', '', 1).isdigit())
        ax.set_title(f'Conectividade {float(connectivity)*100:.0f}%')
        ax.set_xscale('log')
        ax.set_xlabel('Firing rate (Hz)')
        ax.set_xlim(0.1, 10)
        ax.set_xticks([0.01, 0.1, 1, 10, 100])                                     
        ax.set_xticklabels(['0.01', '0.1', '1', '10', '100'])
        ax.set_ylim(0, 1.1)
        ax.legend(frameon=False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    axes[0].set_ylabel('Cell density')

    plt.tight_layout()
    plt.savefig('figures/plots/firing_rate_distribution.jpg', dpi=300, format='jpg')
    plt.close()


firing_rate_distribution(show_mean=True, exclude_single_spike=False)
