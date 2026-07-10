import numpy as np

from utils.data import load_pattern_data
from utils.patterns import activation_degree
from utils.sparsity import gini_index

RUN = 'june_final'

CELL_TYPES = [
    ('mgc',  'mGC'),
    ('igc',  'iGC'),
    ('mc',   'MC'),
    ('hipp', 'HIPP'),
    ('bc',   'BC'),
    ('pca3', 'pCA3'),
    ('ica3', 'iCA3'),
]


def analyse_group(group, trials):
    pooled = {ct: [] for ct, _ in CELL_TYPES}
    activ  = {ct: [] for ct, _ in CELL_TYPES}
    ginis  = {ct: [] for ct, _ in CELL_TYPES}
    n_cells = {}
    n_patterns = 0

    for trial in trials:
        for pattern in trial['patterns']:
            n_patterns += 1
            rates  = pattern['rates']
            counts = pattern.get('spike_counts', {})
            for ct, _ in CELL_TYPES:
                r = np.asarray(rates.get(ct, []), dtype=float)
                if r.size == 0:
                    continue
                pooled[ct].append(r)
                activ[ct].append(activation_degree((r > 0).astype(int)))
                c = np.asarray(counts.get(ct, r), dtype=float)
                ginis[ct].append(gini_index(c))
                n_cells[ct] = r.size

    print(f'\n=== {group} ===  (patterns pooled: {n_patterns})')
    header = (f'{"cell":<5} {"N":>5} {"active%":>8} {"mean_act":>9} '
              f'{"median_act":>11} {"std_act":>8} {"mean_all":>9} {"gini":>7}')
    print(header)
    print('-' * len(header))
    for ct, label in CELL_TYPES:
        if not pooled[ct]:
            continue
        all_rates = np.concatenate(pooled[ct])
        active = all_rates[all_rates > 0]
        mean_act   = active.mean()   if active.size else 0.0
        median_act = np.median(active) if active.size else 0.0
        std_act    = active.std()    if active.size else 0.0
        mean_all   = all_rates.mean()
        activation = 100.0 * np.mean(activ[ct])
        gini       = np.mean(ginis[ct])
        print(f'{label:<5} {n_cells[ct]:>5} {activation:>7.2f}% {mean_act:>9.3f} '
              f'{median_act:>11.3f} {std_act:>8.3f} {mean_all:>9.3f} {gini:>7.3f}')


def main():
    data = load_pattern_data(RUN)
    for group in sorted(data.keys()):
        analyse_group(group, data[group])


if __name__ == '__main__':
    main()
