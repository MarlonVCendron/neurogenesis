import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FuncFormatter
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

from utils.patterns import pattern_separation_degree, pattern_integration_degree, activation_degree, correlation_degree
from utils.data import load_pattern_data
from scipy.stats import mannwhitneyu
import itertools


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

g = list(sorted(list(data.keys())))
groups = np.concatenate((g[1:], g[0:1]))

def in_similarity():
  group_stats = {}
  in_sims = []
  ids = []
  std_errors = []
  for group in groups:
    in_sim_dict = {}
    trial_means_list = []
    for trial in data[group]:
      trial_sims = {}

      original_pattern = trial['original_pattern']
      original_inp = original_pattern['pp_pattern']
      original_out = original_pattern['gc_pattern']

      for pattern in trial['patterns'][:-1]:
        sim = pattern['in_similarity']
        if sim == 0.1:
          continue
        inp = pattern['pp_pattern']
        out = pattern['gc_pattern']
        i_d = pattern_integration_degree(original_inp, inp, original_out, out)
        # i_d = correlation_degree(original_out, out)
        # i_d = correlation_degree(original_inp, inp)
        # t1 = correlation_degree(original_out, out)
        # t2 = correlation_degree(original_inp, inp)
        # i_d = t1 / t2

        if sim not in in_sim_dict:
          in_sim_dict[sim] = []
        if i_d != float("inf") and i_d != np.nan:
          in_sim_dict[sim].append(i_d)

        if sim not in trial_sims:
          trial_sims[sim] = []
        trial_sims[sim].append(i_d)

      trial_means = {sim: np.mean(vals) for sim, vals in trial_sims.items()}
      trial_means_list.append(trial_means)

    group_sim_data = {}
    for trial_mean in trial_means_list:
      for sim, mean_id in trial_mean.items():
        if sim not in group_sim_data:
          group_sim_data[sim] = []
        group_sim_data[sim].append(mean_id)

    # Store for stats
    group_stats[group] = group_sim_data

    average_id = {sim: np.mean(ids) for sim, ids in in_sim_dict.items()}
    std_error = {sim: sem(ids) for sim, ids in in_sim_dict.items()}

    sorted_in_sim = sorted(average_id.keys())
    sorted_average_id = [average_id[sim] for sim in sorted_in_sim]
    sorted_std_error = [std_error[sim] for sim in sorted_in_sim]

    in_sims.append(sorted_in_sim)
    ids.append(sorted_average_id)
    std_errors.append(sorted_std_error)

  fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
  # fig, ax = plt.subplots()

  # ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  ax.xaxis.set_major_formatter(formatter)
  # ax.set_ylim(0, max(max(y) for y in ids)+0.1)
  ax.set_ylim(0, 5.5)

  c_color = "#d64e12"
  cmap = LinearSegmentedColormap.from_list('neuro_cmap', ['#3f6719','#9dd963'])

  # groups_to_skip = ['neurogenesis_0.1', 'neurogenesis_0.2', 'neurogenesis_0.3', 'neurogenesis_0.4', 'neurogenesis_0.6']
  groups_to_skip = []
  total_ng = len(groups) - len(groups_to_skip) - 1
  cmap_index = 0
  # values = zip(in_sims, ids, std_errors)
  for i, (in_sim, id, std_error) in enumerate(zip(in_sims, ids, std_errors)):
    group = groups[i]
    if group in groups_to_skip:
      continue
    if group == 'control':
      color = c_color
      alpha = 0.9
    else:
      # ng_index = float(group.split('_')[1])
      # color = cmap((ng_index - 0.1) / 0.9)
      i = cmap_index / (total_ng-1)
      color = cmap(i)
      cmap_index += 1
      alpha = 0.8

    label = 'Control' if group == 'control' else f'Neurogenesis: {int(float(group.split("_")[1])*100)}% connectivity'
    plt.plot(in_sim, id, color=color, alpha=alpha, label=label)

    plotline, caps, barlinecols = ax.errorbar(
        in_sim,
        id,
        yerr=std_error,
        ecolor=color,
        linestyle='None',
    )
    plt.setp(barlinecols[0], capstyle="round")
    # for capline in lines[1]:
    #   capline.set_capstyle('round')



  plt.legend(frameon=False)

  # sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.1, vmax=1.0))
  # sm.set_array([])
  # cbar = plt.colorbar(sm, ax=plt.gca(), pad=0.1)

  plt.xlabel('Input similarity (%)')
  plt.ylabel('Pattern integration degree ($\\mathcal{I}_D$)')

  plt.tight_layout()
  # plt.show()
  plt.savefig(f'figures/plots/pattern_integration.jpg', dpi=300, format='jpg')
  plt.close()

in_similarity()
