import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

from utils.data import load_pattern_data
from utils.plot_styles import cell_colors, apply_paper_style, panel_label

apply_paper_style()


def collect_rates(data, group, exclude_single_spike=False, include_pca3=False):
    """Return concatenated firing rates (>0) for mgc and igc (and optionally pca3) across all trials/patterns."""
    mgc_rates, igc_rates, pca3_rates = [], [], []
    for trial in data[group]:
        for pattern in trial['patterns']:
            rates = pattern.get('rates', {})
            mgc_r = rates.get('mgc', np.array([]))
            igc_r = rates.get('igc', np.array([]))
            mgc_rates.append(mgc_r[mgc_r > 0])
            igc_rates.append(igc_r[igc_r > 0])
            if include_pca3:
                pca3_r = rates.get('pca3', np.array([]))
                pca3_rates.append(pca3_r[pca3_r > 0])
    mgc = np.concatenate(mgc_rates)
    igc = np.concatenate(igc_rates)
    if exclude_single_spike:
        # cells that fired exactly once all share the same rate (1/duration = min rate)
        if len(mgc): mgc = mgc[mgc > mgc.min()]
        if len(igc): igc = igc[igc > igc.min()]
    if include_pca3:
        pca3 = np.concatenate(pca3_rates) if pca3_rates else np.array([])
        if exclude_single_spike and len(pca3):
            pca3 = pca3[pca3 > pca3.min()]
        return mgc, igc, pca3
    return mgc, igc


def plot_kde(ax, rates, color, label, bw=0.25, show_median=True):
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

    median_rate = np.median(rates)
    if show_median:
        ax.axvline(median_rate, color=color, linestyle='--', linewidth=2, alpha=0.9)
        y_at_median = kde(np.log10(median_rate)) / kde(x_log).max()
        ax.text(
            median_rate, float(y_at_median) + 0.06,
            f'{median_rate:.2f} Hz',
            color=color, fontsize=12, ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.7),
        )
    return median_rate


def draw(fig, spec, data, groups, group=None, label=None, show_median=True,
         exclude_single_spike=False):
    ng_groups = [g for g in groups if 'neurogenesis' in g]
    group = group or ng_groups[0]

    ax = fig.add_subplot(spec)

    mgc_rates, igc_rates = collect_rates(data, group, exclude_single_spike=exclude_single_spike)
    plot_kde(ax, mgc_rates, color=cell_colors['mgc'], label='mGC', bw=0.5, show_median=show_median)
    plot_kde(ax, igc_rates, color=cell_colors['igc'], label='iGC', bw=0.5, show_median=show_median)

    ax.set_xscale('log')
    ax.set_xlabel('Firing rate (Hz)')
    ax.set_xlim(0.1, 10)
    ax.set_xticks([0.1, 1, 10, 100])
    ax.set_xticklabels(['0.1', '1', '10', '100'])
    ax.set_ylim(0, 1.1)
    ax.set_ylabel('Cell density')
    ax.legend(frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if label:
        panel_label(ax, label)

    return ax


def main():
    data = load_pattern_data('rate8')
    groups = sorted(list(data.keys()))

    fig = plt.figure(figsize=(8, 8), dpi=300)
    draw(fig, fig.add_gridspec(1, 1)[0], data, groups)
    # fig.savefig('figures/plots/firing_rate_distribution.jpg', dpi=300, format='jpg')
    fig.savefig('figures/plots/firing_rate_distribution.pdf', format='pdf', bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
