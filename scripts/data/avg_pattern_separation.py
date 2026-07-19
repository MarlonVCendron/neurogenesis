import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem

from utils.patterns import pattern_separation_degree
from utils.data import load_pattern_data
from utils.plot_styles import (
    cell_colors, dense_dots, alpha, igc_connectivity_label,
    apply_paper_style, fig_size, panel_label,
)

apply_paper_style()


def _compute(data, groups):
  sds, i_sds, m_sds = {}, {}, {}
  se, se_i, se_m = {}, {}, {}

  for group in groups:
    in_sim, i_in_sim, m_in_sim = {}, {}, {}
    for trial in data[group]:
      orig = trial['original_pattern']
      o_in = orig['pp_pattern']
      o_out = orig['gc_pattern']
      o_iout = orig['igc_pattern']
      o_mout = orig['mgc_pattern']

      for pattern in trial['patterns'][:-1]:
        sim = pattern['in_similarity']
        inp = pattern['pp_pattern']
        in_sim.setdefault(sim, []).append(pattern_separation_degree(o_in, inp, o_out, pattern['gc_pattern']))
        i_in_sim.setdefault(sim, []).append(pattern_separation_degree(o_in, inp, o_iout, pattern['igc_pattern']))
        m_in_sim.setdefault(sim, []).append(pattern_separation_degree(o_in, inp, o_mout, pattern['mgc_pattern']))

    sds[group]   = np.mean([np.mean(v) for v in in_sim.values()])
    i_sds[group] = np.mean([np.mean(v) for v in i_in_sim.values()])
    m_sds[group] = np.mean([np.mean(v) for v in m_in_sim.values()])
    se[group]    = sem([np.mean(v) for v in in_sim.values()])
    se_i[group]  = sem([np.mean(v) for v in i_in_sim.values()])
    se_m[group]  = sem([np.mean(v) for v in m_in_sim.values()])

  return sds, i_sds, m_sds, se, se_i, se_m


def draw(fig, spec, data, groups, label=None):
  sds, i_sds, m_sds, se, se_i, se_m = _compute(data, groups)

  ax = fig.add_subplot(spec)

  ax.axhline(y=sds[groups[0]], color=cell_colors['control'], linestyle='--', label='Control')
  ax.axhline(y=1, color='gray', linestyle='--')

  ng_groups = groups[1:]
  x = [float(g.split('_')[1]) * 100 for g in ng_groups]

  y   = np.array([sds[g] for g in ng_groups])
  yi  = np.array([i_sds[g] for g in ng_groups])
  ym  = np.array([m_sds[g] for g in ng_groups])
  ey  = np.array([se[g] for g in ng_groups])
  eyi = np.array([se_i[g] for g in ng_groups])
  eym = np.array([se_m[g] for g in ng_groups])

  ax.plot(x, y, color=cell_colors['gc'], label='All GC', alpha=alpha)
  ax.plot(x, yi, color=cell_colors['igc'], label='iGC', alpha=alpha, linestyle=dense_dots)
  ax.plot(x, ym, color=cell_colors['mgc'], label='mGC', alpha=alpha, linestyle=dense_dots)
  ax.fill_between(x, y - ey, y + ey, color=cell_colors['gc'], alpha=0.2)
  ax.fill_between(x, yi - eyi, yi + eyi, color=cell_colors['igc'], alpha=0.2)
  ax.fill_between(x, ym - eym, ym + eym, color=cell_colors['mgc'], alpha=0.2)

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

  fig = plt.figure(figsize=fig_size(0.35, aspect=1.0), dpi=300)
  draw(fig, fig.add_gridspec(1, 1)[0], data, groups)
  # fig.savefig('figures/plots/avg_pattern_separation.jpg', dpi=300, format='jpg', bbox_inches='tight')
  fig.savefig('figures/plots/avg_pattern_separation.pdf', format='pdf', bbox_inches='tight')
  plt.close(fig)


if __name__ == '__main__':
  main()
