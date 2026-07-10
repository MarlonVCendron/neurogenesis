import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem, linregress

from utils.patterns import orthogonalization_degree, correlation_degree, average_activation_degree
from utils.data import load_pattern_data
from utils.plot_styles import cell_colors, alpha, igc_connectivity_label, apply_paper_style, fig_size

apply_paper_style()
np.random.seed(0)

data = load_pattern_data('june_final')
groups = sorted(list(data.keys()))
POPS = [('mgc', 'mgc_pattern'), ('gc', 'gc_pattern'), ('pca3', 'pca3_pattern')]
NULL_SHUFFLES = 8


def _shuffle(v):
  v = np.asarray(v)
  n = int(v.sum())
  s = np.zeros(len(v), dtype=int)
  if n:
    s[np.random.choice(len(v), n, replace=False)] = 1
  return s


def analyse():
  stats = {ct: {} for ct, _ in POPS}
  for group in groups:
    for ct, key in POPS:
      t_logS, t_logO, t_logD, t_rho, t_da, t_null = [], [], [], [], [], []
      for trial in data[group]:
        oin = trial['original_pattern']['pp_pattern']
        oout = trial['original_pattern'][key]
        logS, logO, logD, rho, da, null = [], [], [], [], [], []
        for p in trial['patterns'][:-1]:
          O_in = orthogonalization_degree(oin, p['pp_pattern'])
          O_out = orthogonalization_degree(oout, p[key])
          Da_in = average_activation_degree(oin, p['pp_pattern'])
          Da_out = average_activation_degree(oout, p[key])
          if min(O_in, O_out, Da_in, Da_out) <= 0:
            continue
          logO.append(np.log(O_out / O_in))
          logD.append(np.log(Da_in / Da_out))
          logS.append(np.log((O_out / O_in) * (Da_in / Da_out)))
          rho.append(correlation_degree(oout, p[key]))
          da.append(Da_out)
          null.append(np.mean([orthogonalization_degree(_shuffle(oout), _shuffle(p[key]))
                               for _ in range(NULL_SHUFFLES)]))
        if logS:
          t_logS.append(np.mean(logS))
          t_logO.append(np.mean(logO))
          t_logD.append(np.mean(logD))
          t_rho.append(np.mean(rho))
          t_da.append(np.mean(da))
          t_null.append(np.mean(null))
      if t_logS:
        stats[ct][group] = {
            'logS': (np.mean(t_logS), sem(t_logS)),
            'logO': (np.mean(t_logO), sem(t_logO)),
            'logD': (np.mean(t_logD), sem(t_logD)),
            'rho': np.mean(t_rho), 'da': np.mean(t_da), 'null': np.mean(t_null),
        }
  return stats


def _trend(stats_ct, getter):
  gs = [g for g in groups[1:] if g in stats_ct]
  x = np.array([float(g.split('_')[1]) * 100 for g in gs])
  y = np.array([getter(stats_ct[g]) for g in gs])
  sl, ic, r, p, se = linregress(x, y)
  return sl, r**2, p


def report(stats):
  ng = groups[1:]
  for ct, _ in POPS:
    if not stats[ct]:
      continue
    print(f'\n=================  {ct.upper()}  =================')
    print(f'{"level":>6} {"S_D":>7} {"sparsif":>8} {"decorr":>7} {"rho_out":>8} {"Da_out%":>8} {"nullO":>6}')
    for g in groups:
      if g not in stats[ct]:
        continue
      s = stats[ct][g]
      lvl = 'ctrl' if 'control' in g else g.split('_')[1]
      print(f'{lvl:>6} {np.exp(s["logS"][0]):7.3f} {np.exp(s["logD"][0]):8.3f} '
            f'{np.exp(s["logO"][0]):7.3f} {s["rho"]:8.4f} {100*s["da"]:8.3f} {s["null"]:6.3f}')

    lo, hi = groups[0], ng[-1]
    if lo in stats[ct] and hi in stats[ct]:
      dS = stats[ct][hi]['logS'][0] - stats[ct][lo]['logS'][0]
      dD = stats[ct][hi]['logD'][0] - stats[ct][lo]['logD'][0]
      dO = stats[ct][hi]['logO'][0] - stats[ct][lo]['logO'][0]
      if abs(dS) > 1e-9:
        verb = 'rises' if dS > 0 else 'FALLS'
        print(f'  S_D {verb} control->100%%: {100*dD/dS:.1f}% sparsification + {100*dO/dS:.1f}% decorrelation')
      rho_lo, rho_hi = stats[ct][lo]['rho'], stats[ct][hi]['rho']
      print(f'  rho_out: {rho_lo:.3f} -> {rho_hi:.3f} ({100*(rho_hi-rho_lo)/rho_lo:+.0f}%)')

    for label, getter in [('log S_D', lambda s: s['logS'][0]),
                          ('log sparsif', lambda s: s['logD'][0]),
                          ('log decorr', lambda s: s['logO'][0]),
                          ('null O_out', lambda s: s['null'])]:
      sl, r2, p = _trend(stats[ct], getter)
      print(f'  trend {label:12s} vs excitability: slope={sl:+.5f}  R2={r2:.3f}  p={p:.1e}')


def plot(stats, ct='mgc'):
  """Plot just the orthogonalisation degree (O_out / O_in) of the mGCs vs iGC excitability."""
  ng = [g for g in groups[1:] if g in stats[ct]]
  x = [float(g.split('_')[1]) * 100 for g in ng]

  fig, ax = plt.subplots(figsize=fig_size(0.35, aspect=1.0), dpi=300)

  o_d = np.array([np.exp(stats[ct][g]['logO'][0]) for g in ng])
  lo = np.array([np.exp(stats[ct][g]['logO'][0] - stats[ct][g]['logO'][1]) for g in ng])
  hi = np.array([np.exp(stats[ct][g]['logO'][0] + stats[ct][g]['logO'][1]) for g in ng])

  ctrl = np.exp(stats[ct][groups[0]]['logO'][0])
  ax.axhline(ctrl, color=cell_colors['control'], linestyle='--', label='Control')

  ax.plot(x, o_d, color=cell_colors['mgc'], label='mGC', alpha=alpha)
  ax.fill_between(x, lo, hi, color=cell_colors['mgc'], alpha=0.2)

  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  ax.set_xlabel(igc_connectivity_label)
  ax.set_ylabel('Orthogonalization degree ($\\mathcal{O}_D$)')
  ax.set_xticks(range(10, 101, 10))
  ax.set_xticklabels([10, '', '', 40, '', '', 70, '', '', 100])
  ax.legend(loc='upper left', bbox_to_anchor=(0, 1), frameon=False)

  plt.tight_layout()
  plt.savefig('figures/plots/mgc_orthogonalization.jpg', dpi=300, format='jpg', bbox_inches='tight')
  plt.savefig('figures/plots/mgc_orthogonalization.pdf', format='pdf', bbox_inches='tight')
  plt.close()


stats = analyse()
report(stats)
plot(stats, 'mgc')
