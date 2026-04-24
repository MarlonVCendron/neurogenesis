# AI generated, unverified
import numpy as np
import matplotlib.pyplot as plt

from utils.data import load_pattern_data
from utils.plot_styles import cell_colors

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "lines.linewidth": 4,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

RUN = 'teste_março'
data = load_pattern_data(RUN)
groups = sorted(list(data.keys()))

PREDICTORS = ['pp', 'mgc', 'igc', 'ica3']
SHARED_COLOR = '#aaaaaa'


def _r2(y, y_pred):
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 0.0 if ss_tot == 0 else 1.0 - np.sum((y - y_pred) ** 2) / ss_tot


def ols_r2(X, y):
    """R² of OLS fit with intercept. X can be 1-D or 2-D."""
    X = np.atleast_2d(X)
    if X.shape[0] != len(y):
        X = X.T
    X_b = np.column_stack([np.ones(len(y)), X])
    coeffs, _, _, _ = np.linalg.lstsq(X_b, y, rcond=None)
    return _r2(y, X_b @ coeffs)


def collect(group):
    records = {k: [] for k in PREDICTORS + ['full'] + [f'no_{p}' for p in PREDICTORS]}

    for trial in data[group]:
        vecs = {ct: [] for ct in PREDICTORS + ['pca3']}
        for pattern in trial['patterns']:
            rates = pattern.get('rates', {})
            for ct in vecs:
                vecs[ct].append(np.mean(rates.get(ct, np.zeros(1))))

        vecs = {ct: np.array(v, dtype=float) for ct, v in vecs.items()}
        pca3 = vecs['pca3']
        if np.std(pca3) == 0:
            continue

        pp, mgc, igc, ica3 = vecs['pp'], vecs['mgc'], vecs['igc'], vecs['ica3']
        full_X = np.column_stack([pp, mgc, igc, ica3])

        for p in PREDICTORS:
            records[p].append(ols_r2(vecs[p], pca3))
        records['full'].append(ols_r2(full_X, pca3))

        leave_one_out = {
            'no_pp':   np.column_stack([mgc, igc, ica3]),
            'no_mgc':  np.column_stack([pp,  igc, ica3]),
            'no_igc':  np.column_stack([pp,  mgc, ica3]),
            'no_ica3': np.column_stack([pp,  mgc, igc]),
        }
        for k, X in leave_one_out.items():
            records[k].append(ols_r2(X, pca3))

    n = len(records['full'])
    if n == 0:
        nan_keys = PREDICTORS + ['full'] + [f'uniq_{p}' for p in PREDICTORS] + ['shared']
        return {k: np.nan for k in nan_keys + [f'sem_{k}' for k in nan_keys]}

    result = {}
    for k in PREDICTORS + ['full']:
        arr = np.array(records[k])
        result[f'r2_{k}']  = np.mean(arr)
        result[f'sem_{k}'] = np.std(arr) / np.sqrt(n)

    full_arr = np.array(records['full'])
    total_unique = np.zeros(n)
    for p in PREDICTORS:
        uniq = full_arr - np.array(records[f'no_{p}'])
        result[f'uniq_{p}']  = np.mean(uniq)
        result[f'sem_uniq_{p}'] = np.std(uniq) / np.sqrt(n)
        total_unique += uniq

    shared = full_arr - total_unique
    result['shared']     = np.mean(shared)
    result['sem_shared'] = np.std(shared) / np.sqrt(n)

    return result


def plot():
    ng_groups = groups[1:]
    results   = {g: collect(g) for g in ng_groups}
    x = [float(g.split('_')[1]) * 100 for g in ng_groups]

    def arr(key): return np.array([results[g][key] for g in ng_groups])

    r2  = {p: arr(f'r2_{p}')  for p in PREDICTORS + ['full']}
    sem = {p: arr(f'sem_{p}') for p in PREDICTORS + ['full']}
    uniq     = {p: arr(f'uniq_{p}')     for p in PREDICTORS}
    sem_uniq = {p: arr(f'sem_uniq_{p}') for p in PREDICTORS}
    shared   = arr('shared')

    pred_colors = {
        'pp':   cell_colors['pp'],
        'mgc':  cell_colors['mgc'],
        'igc':  cell_colors['igc'],
        'ica3': cell_colors['ica3'],
        'full': cell_colors['pca3'],
    }
    pred_labels = {
        'pp':   'PP only',
        'mgc':  'mGC only',
        'igc':  'iGC only',
        'ica3': 'iCA3 only',
        'full': 'PP + mGC + iGC + iCA3',
    }

    fig, axes = plt.subplots(1, 2, figsize=(13, 6), dpi=300)
    alpha = 0.85

    # Left: R² lines
    ax = axes[0]
    ax.plot(x, r2['full'], color=pred_colors['full'], label=pred_labels['full'], alpha=alpha, linewidth=5)
    for p in PREDICTORS:
        ax.plot(x, r2[p], color=pred_colors[p], label=pred_labels[p], alpha=alpha, linestyle='--')
        ax.fill_between(x, r2[p] - sem[p], r2[p] + sem[p], color=pred_colors[p], alpha=0.15)
    ax.fill_between(x, r2['full'] - sem['full'], r2['full'] + sem['full'],
                    color=pred_colors['full'], alpha=0.15)
    ax.set_xlabel('Conectividade (%)')
    ax.set_ylabel('R² (var. pCA3 explicada)')
    ax.set_xticks(range(10, 101, 10))
    ax.set_ylim(0, 1)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1.18), frameon=False)

    # Right: stacked unique contributions + shared (clip negatives)
    ax = axes[1]
    stack_data   = [np.clip(uniq[p], 0, None) for p in PREDICTORS]
    stack_data.append(np.clip(shared, 0, None))
    stack_colors = [pred_colors[p] for p in PREDICTORS] + [SHARED_COLOR]
    stack_labels = [f'Exclusivo {p.upper()}' for p in PREDICTORS] + ['Compartilhado']
    ax.stackplot(x, *stack_data, labels=stack_labels, colors=stack_colors, alpha=0.8)
    ax.set_xlabel('Conectividade (%)')
    ax.set_ylabel('R² particionado')
    ax.set_xticks(range(10, 101, 10))
    ax.set_ylim(0, 1)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1.18), frameon=False)

    plt.tight_layout()
    plt.savefig('figures/plots/pca3_variance_partitioning.jpg', dpi=300, format='jpg', bbox_inches='tight')
    plt.savefig('figures/plots/pca3_variance_partitioning.pdf', format='pdf', bbox_inches='tight')
    plt.close()

    print("\n--- Variance partitioning summary (mean across connectivity levels) ---")
    for p in PREDICTORS + ['full']:
        print(f"  R²({p:5s}):       {np.nanmean(r2[p]):.3f}")
    print()
    for p in PREDICTORS:
        print(f"  Unique {p:5s}:    {np.nanmean(uniq[p]):.3f}")
    print(f"  Shared:          {np.nanmean(shared):.3f}")


plot()
