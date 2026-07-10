import os
import sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
import h5py

from scipy.stats import wilcoxon

from utils.sparsity import gini_index
from utils.plot_styles import cell_colors, alpha, apply_paper_style, fig_size

apply_paper_style()

PRE_COLOR  = cell_colors['pp']
POST_COLOR = cell_colors['igc']

RUN_NAME      = 'opto_final_july_positive'
ONSET_TIME_MS = 400
BREAK_TIME_MS = 300.0
WINDOW_MS     = 50.0

CELL_TYPES = [
    ('mgc',  'mGC'),
    ('igc',  'iGC'),
    ('gc',   'all GC'),
    ('pca3', 'pCA3'),
]


def load_data(group_file_path):
    files = sorted(glob(f'{group_file_path}*/**/*.h5', recursive=True))
    if not files:
        sys.exit(f'No .h5 files found under {group_file_path}/')

    runs      = []
    n_neurons = {}
    for fpath in files:
        with h5py.File(fpath, 'r') as f:
            run = {}
            for ct in f['spike_times'].keys():
                times = np.array(f['spike_times'][ct]['times_ms'], dtype=np.float64)
                idx   = np.array(f['spike_times'][ct]['indices'],  dtype=np.int32)
                run[ct] = (times, idx)
                if 'rates' in f and ct in f['rates']:
                    n_neurons[ct] = max(len(f['rates'][ct]), n_neurons.get(ct, 0))
            runs.append(run)
    return runs, n_neurons


def _counts(times_idx, a, b, n):
    times, idx = times_idx
    mask = (times >= a) & (times < b)
    return np.bincount(idx[mask].astype(int), minlength=n)[:n]


def gini_pre_post(runs, n_neurons, onset_abs):
    pre_a,  pre_b  = onset_abs - WINDOW_MS, onset_abs
    post_a, post_b = onset_abs,             onset_abs + WINDOW_MS

    result = {}
    for ct, label in CELL_TYPES:
        pre_vals, post_vals = [], []
        for run in runs:
            if ct == 'gc':
                if 'mgc' not in run:
                    continue
                n_mgc = n_neurons.get('mgc', 0)
                n_igc = n_neurons.get('igc', 0)
                if 'igc' in run and n_igc:
                    pre  = np.concatenate([_counts(run['mgc'], pre_a,  pre_b,  n_mgc),
                                           _counts(run['igc'], pre_a,  pre_b,  n_igc)])
                    post = np.concatenate([_counts(run['mgc'], post_a, post_b, n_mgc),
                                           _counts(run['igc'], post_a, post_b, n_igc)])
                else:
                    pre  = _counts(run['mgc'], pre_a,  pre_b,  n_mgc)
                    post = _counts(run['mgc'], post_a, post_b, n_mgc)
            else:
                if ct not in run or not n_neurons.get(ct, 0):
                    continue
                n    = n_neurons[ct]
                pre  = _counts(run[ct], pre_a,  pre_b,  n)
                post = _counts(run[ct], post_a, post_b, n)
            pre_vals.append(gini_index(pre))
            post_vals.append(gini_index(post))
        if pre_vals:
            result[label] = (np.array(pre_vals), np.array(post_vals))
    return result


def _stars(p):
    return '***' if p < 1e-3 else '**' if p < 1e-2 else '*' if p < 0.05 else 'ns'


def main(group_file_path):
    onset_abs = BREAK_TIME_MS + ONSET_TIME_MS
    runs, n_neurons = load_data(group_file_path)
    res = gini_pre_post(runs, n_neurons, onset_abs)

    labels = list(res)
    pre   = np.array([res[l][0].mean() for l in labels])
    post  = np.array([res[l][1].mean() for l in labels])
    # Paired Wilcoxon signed-rank test (per-run pre vs post)
    pvals = [wilcoxon(res[l][0], res[l][1]).pvalue
             if len(res[l][0]) > 1 and np.any(res[l][0] != res[l][1]) else np.nan
             for l in labels]

    print(f'\nGini sparsity (pre vs post iGC activation) for: {group_file_path}')
    print(f'{"Population":<10} {"pre":>8} {"post":>8} {"delta":>8} {"p":>10}')
    print('-' * 48)
    for l, a, b, p in zip(labels, pre, post, pvals):
        print(f'{l:<10} {a:>8.3f} {b:>8.3f} {b - a:>+8.3f} {p:>10.4g}')

    base_name = os.path.basename(group_file_path)
    try:
        title = f'{int(round(float(base_name.split("_")[1]) * 100))}% excitability'
    except (IndexError, ValueError):
        title = base_name

    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=fig_size(0.32, aspect=0.85), dpi=300)
    ax.bar(x - 0.2, pre,  0.4, label='pre',  color=PRE_COLOR,  alpha=alpha)
    ax.bar(x + 0.2, post, 0.4, label='post', color=POST_COLOR, alpha=alpha)
    for xi, a, b, p in zip(x, pre, post, pvals):
        if not np.isnan(p):
            ax.text(xi, max(a, b) + 0.02, _stars(p), ha='center', va='bottom', fontsize=12)
    ax.set_ylim(0, max(pre.max(), post.max()) * 1.25)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Gini sparsity')
    ax.set_title(title)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()

    out_base = f'figures/plots/optogenetics/opto_sparsity_{base_name}'
    os.makedirs(os.path.dirname(out_base), exist_ok=True)
    fig.savefig(f'{out_base}.pdf', format='pdf', bbox_inches='tight')
    fig.savefig(f'{out_base}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved: {out_base}.pdf')


if __name__ == '__main__':
    base   = f'res/{RUN_NAME}'
    files  = sorted(glob(f'{base}/*'))
    groups = sorted(set(f.split('_ca3')[0] for f in files))
    for group_file_path in groups:
        main(group_file_path)
