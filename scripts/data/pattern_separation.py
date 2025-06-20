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
  sds = []
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
        inp = pattern['pp_pattern']
        out = pattern['gc_pattern']
        s_d = pattern_separation_degree(original_inp, inp, original_out, out)

        if sim not in in_sim_dict:
          in_sim_dict[sim] = []
        if s_d != float("inf") and s_d != np.nan:
          in_sim_dict[sim].append(s_d)

        if sim not in trial_sims:
          trial_sims[sim] = []
        trial_sims[sim].append(s_d)

      trial_means = {sim: np.mean(vals) for sim, vals in trial_sims.items()}
      trial_means_list.append(trial_means)

    group_sim_data = {}
    for trial_mean in trial_means_list:
      for sim, mean_sd in trial_mean.items():
        if sim not in group_sim_data:
          group_sim_data[sim] = []
        group_sim_data[sim].append(mean_sd)

    # Store for stats
    group_stats[group] = group_sim_data

    average_sd = {sim: np.mean(sds) for sim, sds in in_sim_dict.items()}
    std_error = {sim: sem(sds) for sim, sds in in_sim_dict.items()}

    sorted_in_sim = sorted(average_sd.keys())
    sorted_average_sd = [average_sd[sim] for sim in sorted_in_sim]
    sorted_std_error = [std_error[sim] for sim in sorted_in_sim]

    in_sims.append(sorted_in_sim)
    sds.append(sorted_average_sd)
    std_errors.append(sorted_std_error)

  fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
  # fig, ax = plt.subplots()

  # ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  ax.xaxis.set_major_formatter(formatter)
  # ax.set_ylim(0, max(max(y) for y in sds)+0.1)
  ax.set_ylim(0, 6.5)

  c_color = "#d64e12"
  cmap = LinearSegmentedColormap.from_list('neuro_cmap', ['#3f6719','#9dd963'])

  # groups_to_skip = ['neurogenesis_0.1', 'neurogenesis_0.2', 'neurogenesis_0.3', 'neurogenesis_0.4', 'neurogenesis_0.6', 'neurogenesis_0.7', 'neurogenesis_0.8']
  groups_to_skip = []
  total_ng = len(groups) - len(groups_to_skip) - 1
  cmap_index = 0
  # values = zip(in_sims, sds, std_errors)
  for i, (in_sim, sd, std_error) in enumerate(zip(in_sims, sds, std_errors)):
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
    plt.plot(in_sim, sd, color=color, alpha=alpha, label=label)

    plotline, caps, barlinecols = ax.errorbar(
        in_sim,
        sd,
        yerr=std_error,
        ecolor=color,
        linestyle='None',
    )
    plt.setp(barlinecols[0], capstyle="round")
    # for capline in lines[1]:
    #   capline.set_capstyle('round')



  # legend_elements = [
  #     Line2D([0], [0], color=c_color, marker='o'),
  #     Line2D([0], [0], label='Neurogenesis: 10% connectivity', marker='X', color=cmap(0)),
  #     Line2D([0], [0], label='Neurogenesis: 100% connectivity', marker='X', color=cmap(1.0)),
  # ]
  # plt.legend(handles=legend_elements, loc='upper left')

  # sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.1, vmax=1.0))
  # sm.set_array([])
  # cbar = plt.colorbar(sm, ax=plt.gca(), pad=0.1)

  plt.xlabel('Input similarity (%)')
  plt.ylabel('Pattern separation degree ($\\mathcal{S}_D$)')
  plt.axhline(y=1, color='gray', linestyle='--')
  plt.legend(frameon=False)

  plt.tight_layout()
  # plt.show()
  plt.savefig(f'figures/plots/pattern_separation.jpg', dpi=300, format='jpg')
  plt.close()

  # # Statistical analysis
  # control_group = 'control'
  # neuro_groups = [g for g in groups if g != 'control']
  # sim_levels = in_sims[0]  # Assume all groups have same similarity levels

  # print("Statistical Results:")
  # comparisons = list(itertools.product(sim_levels, neuro_groups))
  # alpha = 0.05
  # bonferroni_alpha = alpha / len(comparisons)

  # for sim in sim_levels:
  #   print(f"\nSimilarity {sim:.0%}:")
  #   control_data = group_stats[control_group].get(sim, [])

  #   for ng_group in neuro_groups:
  #     ng_data = group_stats[ng_group].get(sim, [])

  #     if len(control_data) < 2 or len(ng_data) < 2:
  #       print(f"Not enough data for {control_group} vs {ng_group}")
  #       continue

  #     # Mann-Whitney U test
  #     try:
  #       stat, p = mannwhitneyu(control_data, ng_data, alternative='two-sided')
  #     except ValueError:
  #       p = 1.0

  #     # Apply Bonferroni correction
  #     sig = "*" if p < bonferroni_alpha else ""
  #     print(f"{control_group} vs {ng_group}: p = {p:.4f}{sig}")


in_similarity()
