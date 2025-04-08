import math
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
  ids = {}
  i_ids = {}
  m_ids = {}
  pp_ids = {}
  boxplot_data = {}
  std_devs = {}
  for group in groups:
    in_sim_dict = {}
    i_in_sim_dict = {}
    m_in_sim_dict = {}
    pp_in_sim_dict = {}
    for trial in data[group]:
      # for trial in data['control']:
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
        # i_d = pattern_integration_degree(original_inp, inp, original_out, out)
        # i_i_d = pattern_integration_degree(original_inp, inp, original_iout, iout)
        # m_i_d = pattern_integration_degree(original_inp, inp, original_mout, mout)

        i_d = correlation_degree(original_out, out)
        i_i_d = correlation_degree(original_iout, iout)
        m_i_d = correlation_degree(original_mout, mout)
        pp_i_d = correlation_degree(original_inp, inp)

        if sim not in in_sim_dict:
          in_sim_dict[sim] = []
        if not math.isnan(i_d):
          in_sim_dict[sim].append(i_d)

        if sim not in i_in_sim_dict:
          i_in_sim_dict[sim] = []
        if not math.isnan(i_i_d):
          i_in_sim_dict[sim].append(i_i_d)
        
        if sim not in m_in_sim_dict:
          m_in_sim_dict[sim] = []
        if not math.isnan(m_i_d):
          m_in_sim_dict[sim].append(m_i_d)
        
        if sim not in pp_in_sim_dict:
          pp_in_sim_dict[sim] = []
        if not math.isnan(pp_i_d):
          pp_in_sim_dict[sim].append(pp_i_d)
    

    mean_id = np.mean([np.mean(ids) for ids in in_sim_dict.values()])
    mean_i_id = np.mean([np.mean(ids) for ids in i_in_sim_dict.values()])
    mean_m_id = np.mean([np.mean(ids) for ids in m_in_sim_dict.values()])
    mean_pp_id = np.mean([np.mean(ids) for ids in pp_in_sim_dict.values()])
    # mean_id = np.mean([np.mean(ids) for ids in in_sim_dict.values()])
    # mean_i_id = np.mean([np.mean(ids) for ids in i_ids.values()])
    # mean_m_id = np.mean([np.mean(ids) for ids in m_ids.values()])
    # mean_pp_id = np.mean([np.mean(ids) for ids in pp_ids.values()])

    # std_dev = np.std([np.std(sds, ddof=1) for sds in in_sim_dict.values()])
    std_dev = sem([np.mean(sds) for sds in in_sim_dict.values()])

    ids[group] = mean_id / mean_pp_id
    i_ids[group] = mean_i_id / mean_pp_id
    m_ids[group] = mean_m_id / mean_pp_id
    boxplot_data[group] = [np.mean(sds) for sds in in_sim_dict.values()]
    std_devs[group] = std_dev
  
  fig, ax = plt.subplots()

  c_color = "#d64e12"
  cmap = LinearSegmentedColormap.from_list('neuro_cmap', ["#16a4d8", '#8bd346'])


  ids = [ids[group] for group in groups]
  i_ids = [i_ids[group] for group in groups]
  m_ids = [m_ids[group] for group in groups]
  
  # plt.gca().set_aspect('equal')

  # groups_indices = np.arange(len(sorted_groups))
  # points = np.array([groups_indices, sorted_sds]).T.reshape(-1, 1, 2)
  # segments = np.concatenate([points[:-1], points[1:]], axis=1)
  
  # # Create a LineCollection
  # lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(min(sorted_sds), max(sorted_sds)))
  # lc.set_array(sorted_sds)  # Set the values used for colormapping
  # line = plt.gca().add_collection(lc)

  # plt.scatter(groups_indices, sorted_sds, c=sorted_sds, cmap=cmap, label=group)

  print(i_ids)
  plt.axhline(y=ids[0], color=c_color, linestyle='--', label='Control')
  
  alpha = 0.85
  plt.plot(groups[1:], ids[1:], color='#8bd346', label='Full GC population pattern', marker='o', alpha=alpha)
  plt.plot(groups[1:], i_ids[1:], color='#16a4d8', label='iGC pattern', marker='o', alpha=alpha)
  plt.plot(groups[1:], m_ids[1:], color='#9b5fe0', label='mGC pattern', marker='o', alpha=alpha)

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

  plt.title('Average pattern integration degree ($\\mathcal{I}_D$) by group and population')
  plt.xlabel('Groups')
  plt.ylabel('$\\mathcal{I}_D$')
  # plt.axhline(y=1, color='gray', linestyle='--')

  xlabels = ['Ng 10%', 'Ng 20%', 'Ng 30%', 'Ng 40%', 'Ng 50%', 'Ng 60%', 'Ng 70%', 'Ng 80%', 'Ng 90%', 'Ng 100%']
  plt.xticks(ticks=range(len(xlabels)), labels=xlabels)
  # plt.legend()

  plt.show()


in_similarity()
