import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem, linregress

from utils.patterns import pattern_separation_degree
from utils.data import load_pattern_data
from utils.plot_styles import cell_colors, alpha, linewidth, igc_connectivity_label

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "lines.linewidth": linewidth,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

RUN = 'april_2026'
data = load_pattern_data(RUN)
groups = sorted(list(data.keys()))


def collect(group):
    ca3_sds, mgc_sds, igc_sds = {}, {}, {}
    for trial in data[group]:
        orig = trial['original_pattern']
        orig_pp   = orig['pp_pattern']
        orig_ca3  = orig['pca3_pattern']
        orig_mgc  = orig['mgc_pattern']
        orig_igc  = orig['igc_pattern']

        for pattern in trial['patterns'][:-1]:
            sim = pattern['in_similarity']
            pp  = pattern['pp_pattern']

            ca3_sds.setdefault(sim, []).append(pattern_separation_degree(orig_pp, pp, orig_ca3,  pattern['pca3_pattern']))
            mgc_sds.setdefault(sim, []).append(pattern_separation_degree(orig_pp, pp, orig_mgc,  pattern['mgc_pattern']))
            igc_sds.setdefault(sim, []).append(pattern_separation_degree(orig_pp, pp, orig_igc,  pattern['igc_pattern']))

    mean = lambda d: np.mean([np.mean(v) for v in d.values()])
    se   = lambda d: sem([np.mean(v) for v in d.values()])
    return (mean(ca3_sds), mean(mgc_sds), mean(igc_sds), se(ca3_sds),   se(mgc_sds),   se(igc_sds))

def plot():
    results = {g: collect(g) for g in groups}

    control_group = groups[groups.index('control_ca3')]
    control_sd = results[control_group][0]
    ng_groups  = groups[1:]
    x = [float(g.split('_')[1]) * 100 for g in ng_groups]

    print('neurogenesis groups', ng_groups)
    ca3, mgc, igc = zip(*[(results[g][0], results[g][1], results[g][2]) for g in ng_groups])
    sem_ca3, sem_mgc, sem_igc = zip(*[(results[g][3], results[g][4], results[g][5]) for g in ng_groups])
    ca3, mgc, igc = np.array(ca3), np.array(mgc), np.array(igc)
    sem_ca3, sem_mgc, sem_igc = np.array(sem_ca3), np.array(sem_mgc), np.array(sem_igc)

    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    ax.axhline(y=control_sd, color=cell_colors['control'], linestyle='--', label='Control')
    # ax.axhline(y=1, color='gray', linestyle='--')

    print(x)
    print(ca3)
    ax.plot(x, ca3, color=cell_colors['pca3'], label='pCA3', alpha=alpha)
    # ax.plot(x, mgc, color=cell_colors['mgc'],  label='mGC', alpha=alpha, linestyle=dense_dots)
    # ax.plot(x, igc, color=cell_colors['igc'],  label='iGC', alpha=alpha, linestyle=dense_dots)
    ax.fill_between(x, ca3 - sem_ca3, ca3 + sem_ca3, color=cell_colors['pca3'], alpha=0.2)
    # ax.fill_between(x, mgc - sem_mgc, mgc + sem_mgc, color=cell_colors['mgc'],  alpha=0.2)
    # ax.fill_between(x, igc - sem_igc, igc + sem_igc, color=cell_colors['igc'],  alpha=0.2)

    slope, intercept, r, p, _ = linregress(x, ca3)
    print(f"pCA3 S_D: slope={slope:.4f}, R²={r**2:.4f}, p={p:.4f}")

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel(igc_connectivity_label)
    ax.set_ylabel('Pattern separation degree ($\\mathcal{S}_D$)')
    ax.set_xticks(ticks=range(10, 101, 10), labels=[10, '', '', 40, '', '', 70, '', '', 100])
    # ax.set_xlim(5, 105)
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1), frameon=False)

    plt.tight_layout()

    plt.savefig('figures/plots/pattern_separation_ca3.jpg', dpi=300, format='jpg', bbox_inches='tight')
    plt.savefig('figures/plots/pattern_separation_ca3.pdf', format='pdf', bbox_inches='tight')
    plt.close()


plot()
