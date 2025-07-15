import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

from utils.patterns import pattern_separation_degree
from utils.data import load_pattern_data
from utils.plot_styles import cell_colors, dense_dots

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    # "font.size": 16,
    # "axes.titlesize": 23,
    # "axes.labelsize": 22,
    # "xtick.labelsize": 16,
    # "ytick.labelsize": 16,
    # "legend.fontsize": 20,

    "lines.linewidth": 6,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

data = load_pattern_data('run_projeto_banca_final')

groups = sorted(list(data.keys()))

def in_similarity():
  sds = {}
  i_sds = {}
  m_sds = {}
  sems = {}
  sems_i = {}
  sems_m = {}
  for group in groups:
    in_sim_dict = {}
    i_in_sim_dict = {}
    m_in_sim_dict = {}
    for trial in data[group]:
      original_inp = trial['original_pattern']['pp_pattern']
      original_out = trial['original_pattern']['gc_pattern']
      original_iout = trial['original_pattern']['igc_pattern']
      original_mout = trial['original_pattern']['mgc_pattern']

      for pattern in trial['patterns'][:-1]:
        sim = pattern['in_similarity']
        inp = pattern['pp_pattern']
        out = pattern['gc_pattern']
        iout = pattern['igc_pattern']
        mout = pattern['mgc_pattern']

        s_d = pattern_separation_degree(original_inp, inp, original_out, out)
        i_s_d = pattern_separation_degree(original_inp, inp, original_iout, iout)
        m_s_d = pattern_separation_degree(original_inp, inp, original_mout, mout)

        if sim not in in_sim_dict:
          in_sim_dict[sim] = []
        in_sim_dict[sim].append(s_d)

        if sim not in i_in_sim_dict:
          i_in_sim_dict[sim] = []
        i_in_sim_dict[sim].append(i_s_d)

        if sim not in m_in_sim_dict:
          m_in_sim_dict[sim] = []
        m_in_sim_dict[sim].append(m_s_d)

    mean_sd = np.mean([np.mean(sds) for sds in in_sim_dict.values()])
    mean_i_sd = np.mean([np.mean(sds) for sds in i_in_sim_dict.values()])
    mean_m_sd = np.mean([np.mean(sds) for sds in m_in_sim_dict.values()])

    std_error = sem([np.mean(sds) for sds in in_sim_dict.values()])
    std_error_i = sem([np.mean(sds) for sds in i_in_sim_dict.values()])
    std_error_m = sem([np.mean(sds) for sds in m_in_sim_dict.values()])

    sds[group] = mean_sd
    i_sds[group] = mean_i_sd
    m_sds[group] = mean_m_sd
    
    sems[group] = std_error
    sems_i[group] = std_error_i
    sems_m[group] = std_error_m
  
  fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
  # fig, ax = plt.subplots()

  cmap = LinearSegmentedColormap.from_list('neuro_cmap', ["#16a4d8", '#8bd346'])


  sds = [sds[group] for group in groups]
  i_sds = [i_sds[group] for group in groups]
  m_sds = [m_sds[group] for group in groups]

  sems = [sems[group] for group in groups]
  sems_i = [sems_i[group] for group in groups]
  sems_m = [sems_m[group] for group in groups]
  
  # plt.gca().set_aspect('equal')

  # groups_indices = np.arange(len(sorted_groups))
  # points = np.array([groups_indices, sorted_sds]).T.reshape(-1, 1, 2)
  # segments = np.concatenate([points[:-1], points[1:]], axis=1)
  
  # # Create a LineCollection
  # lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(min(sorted_sds), max(sorted_sds)))
  # lc.set_array(sorted_sds)  # Set the values used for colormapping
  # line = plt.gca().add_collection(lc)

  # plt.scatter(groups_indices, sorted_sds, c=sorted_sds, cmap=cmap, label=group)

  print(sds)
  plt.axhline(y=sds[0], color=cell_colors['control'], linestyle='--')
  plt.axhline(y=1, color='gray', linestyle='--')
  # ax.set_ylim(0, 6.5)
  
  ng_groups = groups[1:]
  sds = sds[1:]
  i_sds = i_sds[1:]
  m_sds = m_sds[1:]

  sems = sems[1:]
  sems_i = sems_i[1:]
  sems_m = sems_m[1:]

  alpha = 0.8
  plt.plot(ng_groups, sds, color=cell_colors['gc'], label='Total GC', alpha=alpha)
  plt.plot(ng_groups, i_sds, color=cell_colors['igc'], label='iGC', alpha=alpha, linestyle=dense_dots)
  plt.plot(ng_groups, m_sds, color=cell_colors['mgc'], label='mGC', alpha=alpha, linestyle=dense_dots)

  sds, i_sds, m_sds = np.array(sds), np.array(i_sds), np.array(m_sds)
  sems, sems_i, sems_m = np.array(sems), np.array(sems_i), np.array(sems_m)

  plt.fill_between(ng_groups, sds - sems, sds + sems, color=cell_colors['gc'], alpha=0.2)
  plt.fill_between(ng_groups, i_sds - sems_i, i_sds + sems_i, color=cell_colors['igc'], alpha=0.2)
  plt.fill_between(ng_groups, m_sds - sems_m, m_sds + sems_m, color=cell_colors['mgc'], alpha=0.2)

  # ax.boxplot(
  #     sorted_boxplot_data,
  #     positions=range(len(sorted_groups)),
  #     widths=0.1,
  #     patch_artist=True,
  #     boxprops=dict(facecolor="#16a4d8"),
  #     medianprops=dict(color="#d64e12"),
  #     showmeans=False,
  #     meanprops=dict(marker="D", markeredgecolor="black", markerfacecolor="gold")
  # )

  # sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.1, vmax=1.0))
  # sm.set_array([])
  # cbar = plt.colorbar(sm, ax=plt.gca(), pad=0.1)

  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)

  # plt.title('Average pattern separation degree ($\\mathcal{S}_D$) by group and population')
  plt.xlabel('Modelos de neurogênese com X% de conectividade')
  plt.ylabel('Grau de separação de padrões ($\\mathcal{S}_D$)')
  # plt.axhline(y=1, color='gray', linestyle='--')

  xlabels = range(20, 101, 20)
  plt.xticks(ticks=range(1, 10, 2), labels=xlabels)
  plt.legend(loc='upper left', bbox_to_anchor=(0, 1.15), frameon=False)

  # plt.show()
  plt.tight_layout()
  plt.savefig(f'figures/plots/avg_pattern_separation.jpg', dpi=300, format='jpg', bbox_inches='tight')
  plt.savefig(f'figures/plots/avg_pattern_separation.pdf', format='pdf', bbox_inches='tight')
  plt.close()


in_similarity()
