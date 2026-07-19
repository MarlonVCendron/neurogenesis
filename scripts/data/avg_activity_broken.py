import numpy as np
from matplotlib.ticker import FuncFormatter, MaxNLocator
import matplotlib.pyplot as plt
from scipy.stats import sem

from utils.patterns import activation_degree
from utils.data import load_pattern_data
from utils.plot_styles import (
    cell_colors, dense_dots, alpha, igc_connectivity_label,
    apply_paper_style, fig_size, panel_label,
)

apply_paper_style()


def _compute(data, groups):
  ads, iads, mads = {}, {}, {}
  se, se_i, se_m = {}, {}, {}

  for group in groups:
    in_sim, i_in_sim, m_in_sim = {}, {}, {}
    for trial in data[group]:
      for pattern in trial['patterns'][:-1]:
        sim = pattern['in_similarity']
        in_sim.setdefault(sim, []).append(activation_degree(pattern['gc_pattern']))
        i_in_sim.setdefault(sim, []).append(activation_degree(pattern['igc_pattern']))
        m_in_sim.setdefault(sim, []).append(activation_degree(pattern['mgc_pattern']))

    ads[group]  = np.mean([np.mean(v) for v in in_sim.values()])
    iads[group] = np.mean([np.mean(v) for v in i_in_sim.values()])
    mads[group] = np.mean([np.mean(v) for v in m_in_sim.values()])
    se[group]   = sem([np.mean(v) for v in in_sim.values()])
    se_i[group] = sem([np.mean(v) for v in i_in_sim.values()])
    se_m[group] = sem([np.mean(v) for v in m_in_sim.values()])

  return ads, iads, mads, se, se_i, se_m


def draw(fig, spec, data, groups, label=None):
  ads, iads, mads, se, se_i, se_m = _compute(data, groups)

  inner = spec.subgridspec(2, 1, hspace=0.05)
  ax = fig.add_subplot(inner[0])
  ax2 = fig.add_subplot(inner[1], sharex=ax)

  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  for axis in (ax, ax2):
    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_major_formatter(formatter)

  control = ads[groups[0]]
  for axis in (ax, ax2):
    axis.axhline(y=control, color=cell_colors['control'], linestyle='--', label='Control')

  ng_groups = groups[1:]
  ng_x = np.array([float(g.split('_')[1]) for g in ng_groups])

  ads_d  = np.array([ads[g] for g in ng_groups])
  iads_d = np.array([iads[g] for g in ng_groups])
  mads_d = np.array([mads[g] for g in ng_groups])
  se_d   = np.array([se[g] for g in ng_groups])
  se_i_d = np.array([se_i[g] for g in ng_groups])
  se_m_d = np.array([se_m[g] for g in ng_groups])

  for axis in (ax, ax2):
    axis.plot(ng_x, ads_d, color=cell_colors['gc'], label='All GC', marker='', alpha=alpha)
    axis.plot(ng_x, iads_d, color=cell_colors['igc'], label='iGC', marker='', alpha=alpha, linestyle=dense_dots)
    axis.plot(ng_x, mads_d, color=cell_colors['mgc'], label='mGC', marker='', alpha=alpha, linestyle=dense_dots)
    axis.fill_between(ng_x, ads_d - se_d, ads_d + se_d, color=cell_colors['gc'], alpha=0.2)
    axis.fill_between(ng_x, iads_d - se_i_d, iads_d + se_i_d, color=cell_colors['igc'], alpha=0.2)
    axis.fill_between(ng_x, mads_d - se_m_d, mads_d + se_m_d, color=cell_colors['mgc'], alpha=0.2)

  lo = np.min(np.concatenate([ads_d - se_d, iads_d - se_i_d, mads_d - se_m_d]))
  hi = np.max(np.concatenate([ads_d + se_d, iads_d + se_i_d, mads_d + se_m_d]))
  ax.set_ylim(.20, hi * 1.05)
  ax2.set_ylim(lo * .95, .09)

  ax.spines['bottom'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  ax2.spines['top'].set_visible(False)
  ax2.spines['right'].set_visible(False)
  ax.xaxis.set_visible(False)
  ax2.xaxis.tick_bottom()

  d = .015
  kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
  ax.plot((-d, +d), (-d, +d), **kwargs)
  kwargs.update(transform=ax2.transAxes)
  ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)

  ax.legend(frameon=False)

  ax2.set_xlabel(igc_connectivity_label)
  ax2.set_xticks(np.arange(0.1, 1.1, 0.1))
  ax2.set_xticklabels([10, '', '', 40, '', '', 70, '', '', 100])

  host = fig.add_subplot(spec, frameon=False)
  host.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
  host.set_xticks([])
  host.set_yticks([])
  host.set_ylabel('Mean population activation (%)', labelpad=30)

  if label:
    panel_label(ax, label)

  return ax, ax2


def main():
  data = load_pattern_data('june_final')
  groups = sorted(list(data.keys()))

  fig = plt.figure(figsize=fig_size(0.35, aspect=1.0), dpi=300)
  draw(fig, fig.add_gridspec(1, 1)[0], data, groups)
  # fig.savefig('figures/plots/avg_activity.jpg', dpi=300, format='jpg', bbox_inches='tight')
  fig.savefig('figures/plots/avg_activity.pdf', format='pdf', bbox_inches='tight')
  plt.close(fig)


if __name__ == '__main__':
  main()
