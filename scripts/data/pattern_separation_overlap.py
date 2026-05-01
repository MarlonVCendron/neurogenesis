# AI generated, unverified
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem, linregress

from utils.data import load_pattern_data
from utils.plot_styles import cell_colors, dense_dots, alpha, igc_connectivity_label, linewidth

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


def jaccard(a, b):
    a, b = np.asarray(a, dtype=bool), np.asarray(b, dtype=bool)
    intersection = np.sum(a & b)
    union = np.sum(a | b)
    if union == 0:
        return 0.0
    return float(intersection / union)


def separation_power(in_1, in_2, out_1, out_2):
    oi_in  = jaccard(in_1, in_2)
    oi_out = jaccard(out_1, out_2)
    if oi_in == 0:
        return 0.0
    return (oi_in - oi_out) / oi_in * 100.0


def collect(group):
    sds, i_sds, m_sds = {}, {}, {}
    for trial in data[group]:
        orig = trial['original_pattern']
        for pattern in trial['patterns'][:-1]:
            sim = pattern['in_similarity']
            sds.setdefault(sim, []).append(separation_power(
                orig['pp_pattern'], pattern['pp_pattern'],
                orig['gc_pattern'], pattern['gc_pattern']))
            i_sds.setdefault(sim, []).append(separation_power(
                orig['pp_pattern'], pattern['pp_pattern'],
                orig['igc_pattern'], pattern['igc_pattern']))
            m_sds.setdefault(sim, []).append(separation_power(
                orig['pp_pattern'], pattern['pp_pattern'],
                orig['mgc_pattern'], pattern['mgc_pattern']))

    mean = lambda d: np.mean([np.mean(v) for v in d.values()])
    se   = lambda d: sem([np.mean(v) for v in d.values()])
    return (mean(sds), mean(i_sds), mean(m_sds),
            se(sds),   se(i_sds),   se(m_sds))


def plot():
    results = {g: collect(g) for g in groups}

    control_sd = results[groups[0]][0]
    ng_groups  = groups[1:]
    x = [float(g.split('_')[1]) * 100 for g in ng_groups]

    sds,   i_sds,   m_sds   = zip(*[(results[g][0], results[g][1], results[g][2]) for g in ng_groups])
    sems,  sems_i,  sems_m  = zip(*[(results[g][3], results[g][4], results[g][5]) for g in ng_groups])
    sds, i_sds, m_sds = np.array(sds), np.array(i_sds), np.array(m_sds)
    sems, sems_i, sems_m = np.array(sems), np.array(sems_i), np.array(sems_m)

    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
    ax.axhline(y=control_sd, color=cell_colors['control'], linestyle='--', label='Control')
    ax.axhline(y=0, color='gray', linestyle='--')

    # ax.plot(x, sds,   color=cell_colors['gc'],  label='All GC', alpha=alpha)
    # ax.plot(x, i_sds, color=cell_colors['igc'], label='iGC',      alpha=alpha, linestyle=dense_dots)
    ax.plot(x, m_sds, color=cell_colors['mgc'], label='mGC',      alpha=alpha, linestyle=dense_dots)
    # ax.fill_between(x, sds   - sems,   sds   + sems,   color=cell_colors['gc'],  alpha=0.2)
    # ax.fill_between(x, i_sds - sems_i, i_sds + sems_i, color=cell_colors['igc'], alpha=0.2)
    ax.fill_between(x, m_sds - sems_m, m_sds + sems_m, color=cell_colors['mgc'], alpha=0.2)

    slope, intercept, r, p, _ = linregress(x, m_sds)
    print(f"mGC Separation Power: slope={slope:.4f}, R²={r**2:.4f}, p={p:.4f}")

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel(igc_connectivity_label)
    ax.set_ylabel('jaccard (SP, %)')
    ax.set_xticks(range(10, 101, 10))
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1.15), frameon=False)
    plt.tight_layout()
    plt.savefig('figures/plots/pattern_separation_overlap.jpg', dpi=300, format='jpg', bbox_inches='tight')
    plt.savefig('figures/plots/pattern_separation_overlap.pdf', format='pdf', bbox_inches='tight')
    plt.close()


plot()
