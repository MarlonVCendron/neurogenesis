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

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 16,
    "axes.titlesize": 23,
    "axes.labelsize": 22,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 20,

    "lines.linewidth": 5,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

data = load_pattern_data('izhikevich_run_01')

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
  
  fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
  # fig, ax = plt.subplots()

  c_color = "#d64e12"
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
  plt.axhline(y=sds[0], color=c_color, linestyle='--')
  plt.axhline(y=1, color='gray', linestyle='--')
  # ax.set_ylim(0, 6.5)
  
  ng_groups = groups[1:]
  sds = sds[1:]
  i_sds = i_sds[1:]
  m_sds = m_sds[1:]

  alpha = 0.8
  plt.plot(ng_groups, sds, color='#8bd346', label='Full GC population pattern', alpha=alpha)
  plt.plot(ng_groups, i_sds, color='#16a4d8', label='iGC pattern', alpha=alpha)
  plt.plot(ng_groups, m_sds, color='#9b5fe0', label='mGC pattern', alpha=alpha)

  _,_,barlinecols = ax.errorbar(
      ng_groups,
      sds,
      yerr=sems[1:],
      ecolor='#8bd346',
      alpha=alpha,
      linestyle='None'
  )
  plt.setp(barlinecols[0], capstyle="round")

  _,_,barlinecols = ax.errorbar(
      ng_groups,
      i_sds,
      yerr=sems_i[1:],
      ecolor='#16a4d8',
      alpha=alpha,
      linestyle='None'
  )
  plt.setp(barlinecols[0], capstyle="round")

  _,_,barlinecols = ax.errorbar(
      ng_groups,
      m_sds,
      yerr=sems_m[1:],
      ecolor='#9b5fe0',
      alpha=alpha,
      linestyle='None'
  )
  plt.setp(barlinecols[0], capstyle="round")

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

  # plt.title('Average pattern separation degree ($\\mathcal{S}_D$) by group and population')
  plt.xlabel('Neurogenesis models with X% connectivity fraction')
  plt.ylabel('')
  # plt.axhline(y=1, color='gray', linestyle='--')

  xlabels = range(10, 101, 10)
  plt.xticks(ticks=range(len(xlabels)), labels=xlabels)
  plt.legend(frameon=False)

  # plt.show()
  plt.savefig(f'figures/plots/avg_pattern_separation.jpg', dpi=300, format='jpg')
  plt.close()


in_similarity()
