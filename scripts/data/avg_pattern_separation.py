import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

from utils.patterns import pattern_separation_degree, activation_degree, correlation_degree, pattern_integration_degree
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

    "lines.linewidth": 3,
})

data = load_pattern_data('run_05')

groups = sorted(list(data.keys()))

def in_similarity():
  sds = {}
  i_sds = {}
  m_sds = {}
  boxplot_data = {}
  std_devs = {}
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
        i_s_d = pattern_integration_degree(original_inp, inp, original_iout, iout)
        m_s_d = pattern_integration_degree(original_inp, inp, original_mout, mout)

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

    # std_dev = np.std([np.std(sds, ddof=1) for sds in in_sim_dict.values()])
    std_dev = sem([np.mean(sds) for sds in in_sim_dict.values()])

    sds[group] = mean_sd
    i_sds[group] = mean_i_sd
    m_sds[group] = mean_m_sd
    boxplot_data[group] = [np.mean(sds) for sds in in_sim_dict.values()]
    std_devs[group] = std_dev
  
  fig, ax = plt.subplots()

  c_color = "#d64e12"
  cmap = LinearSegmentedColormap.from_list('neuro_cmap', ["#16a4d8", '#8bd346'])


  sds = [sds[group] for group in groups]
  i_sds = [i_sds[group] for group in groups]
  m_sds = [m_sds[group] for group in groups]
  
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
  plt.axhline(y=sds[0], color=c_color, linestyle='--', label='Control')
  plt.axhline(y=1, color='gray', linestyle='--')
  
  alpha = 0.85
  plt.plot(groups[1:], sds[1:], color='#8bd346', label='Full GC population pattern', marker='o', alpha=alpha)
  plt.plot(groups[1:], i_sds[1:], color='#16a4d8', label='iGC pattern', marker='o', alpha=alpha)
  plt.plot(groups[1:], m_sds[1:], color='#9b5fe0', label='mGC pattern', marker='o', alpha=alpha)
  
  plt.legend()
  # lc = LineCollection(segments, cmap=cmap, norm=norm)
  # lc.set_array(x)
  # lc.set_linewidth(2)

  # line = ax.add_collection(lc)



  # ax.errorbar(
  #     sorted_groups,
  #     sorted_sds,
  #     yerr=sorted_std_devs,
  #     # color=color
  # )

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

  # Add a colorbar to show the gradient scale
  sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.1, vmax=1.0))
  sm.set_array([])
  # cbar = plt.colorbar(sm, ax=plt.gca(), pad=0.1)

  plt.title('Average pattern separation degree ($\\mathcal{S}_D$) by group and population')
  plt.xlabel('Groups')
  plt.ylabel('$\\mathcal{S}_D$')
  # plt.axhline(y=1, color='gray', linestyle='--')

  xlabels = ['Ng 10%', 'Ng 20%', 'Ng 30%', 'Ng 40%', 'Ng 50%', 'Ng 60%', 'Ng 70%', 'Ng 80%', 'Ng 90%', 'Ng 100%']
  plt.xticks(ticks=range(len(xlabels)), labels=xlabels)
  # plt.legend()

  plt.show()


in_similarity()
