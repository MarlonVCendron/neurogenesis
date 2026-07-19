import numpy as np
from matplotlib.ticker import FuncFormatter, MultipleLocator
import matplotlib.pyplot as plt
from scipy.stats import sem

from utils.patterns import activation_degree
from utils.data import load_pattern_data
from utils.plot_styles import (
    cell_colors, alpha, igc_connectivity_label,
    apply_paper_style, fig_size, panel_label,
)

apply_paper_style()


def _compute(data, groups):
  cads, se = {}, {}

  for group in groups:
    c_in_sim = {}
    for trial in data[group]:
      for pattern in trial['patterns'][:-1]:
        c_in_sim.setdefault(pattern['in_similarity'], []).append(activation_degree(pattern['pca3_pattern']))

    cads[group] = np.mean([np.mean(v) for v in c_in_sim.values()])
    se[group]   = sem([np.mean(v) for v in c_in_sim.values()])

  return cads, se


def draw(fig, spec, data, groups, label=None):
  cads, se = _compute(data, groups)

  ax = fig.add_subplot(spec)

  ax.yaxis.set_major_locator(MultipleLocator(0.03))
  ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{round(y*100)}'))

  ng_groups = groups[1:]
  y = np.array([cads[g] for g in ng_groups])
  e = np.array([se[g] for g in ng_groups])
  x = range(len(ng_groups))

  ax.axhline(y=cads[groups[0]], color=cell_colors['control'], linestyle='--', label='Control')
  ax.plot(x, y, color=cell_colors['pca3'], label='pCA3', marker='', alpha=alpha)
  ax.fill_between(x, y - e, y + e, color=cell_colors['pca3'], alpha=0.2)

  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)

  pad = 0.2
  ax.set_ylim((1 - pad) * y.min(), (1 + pad) * y.max())
  ax.legend(frameon=False)

  ax.set_ylabel('Mean population activation (%)')
  ax.set_xlabel(igc_connectivity_label)
  ax.set_xticks(range(len(ng_groups)))
  ax.set_xticklabels([10, '', '', 40, '', '', 70, '', '', 100])

  if label:
    panel_label(ax, label)

  return ax


def main():
  data = load_pattern_data('june_final')
  groups = sorted(list(data.keys()))

  fig = plt.figure(figsize=fig_size(0.35, aspect=2/3), dpi=300)
  draw(fig, fig.add_gridspec(1, 1)[0], data, groups)
  # fig.savefig('figures/plots/avg_activity_ca3.jpg', dpi=300, format='jpg', bbox_inches='tight')
  fig.savefig('figures/plots/avg_activity_ca3.pdf', format='pdf', bbox_inches='tight')
  plt.close(fig)


if __name__ == '__main__':
  main()
