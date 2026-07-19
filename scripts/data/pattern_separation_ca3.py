import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem

from utils.patterns import pattern_separation_degree
from utils.data import load_pattern_data
from utils.plot_styles import (
    cell_colors, alpha, igc_connectivity_label,
    apply_paper_style, fig_size, panel_label,
)

apply_paper_style()


def _collect(data, group):
  ca3_sds = {}
  for trial in data[group]:
    orig = trial['original_pattern']
    o_pp = orig['pp_pattern']
    o_ca3 = orig['pca3_pattern']

    for pattern in trial['patterns'][:-1]:
      sim = pattern['in_similarity']
      ca3_sds.setdefault(sim, []).append(
          pattern_separation_degree(o_pp, pattern['pp_pattern'], o_ca3, pattern['pca3_pattern']))

  mean = np.mean([np.mean(v) for v in ca3_sds.values()])
  se = sem([np.mean(v) for v in ca3_sds.values()])
  return mean, se


def draw(fig, spec, data, groups, label=None):
  results = {g: _collect(data, g) for g in groups}

  control_sd = results['control_ca3'][0]
  ng_groups = groups[1:]
  x = [float(g.split('_')[1]) * 100 for g in ng_groups]
  ca3 = np.array([results[g][0] for g in ng_groups])
  se = np.array([results[g][1] for g in ng_groups])

  ax = fig.add_subplot(spec)
  ax.axhline(y=control_sd, color=cell_colors['control'], linestyle='--', label='Control')

  ax.plot(x, ca3, color=cell_colors['pca3'], label='pCA3', alpha=alpha)
  ax.fill_between(x, ca3 - se, ca3 + se, color=cell_colors['pca3'], alpha=0.2)

  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  ax.set_xlabel(igc_connectivity_label)
  ax.set_ylabel('Pattern separation degree ($\\mathcal{S}_D$)')
  ax.set_xticks(range(10, 101, 10))
  ax.set_xticklabels([10, '', '', 40, '', '', 70, '', '', 100])
  ax.legend(loc='upper left', bbox_to_anchor=(0, 1), frameon=False)

  if label:
    panel_label(ax, label)

  return ax


def main():
  data = load_pattern_data('june_final')
  groups = sorted(list(data.keys()))

  fig = plt.figure(figsize=fig_size(0.35, aspect=2/3), dpi=300)
  draw(fig, fig.add_gridspec(1, 1)[0], data, groups)
  # fig.savefig('figures/plots/pattern_separation_ca3.jpg', dpi=300, format='jpg', bbox_inches='tight')
  fig.savefig('figures/plots/pattern_separation_ca3.pdf', format='pdf', bbox_inches='tight')
  plt.close(fig)


if __name__ == '__main__':
  main()
