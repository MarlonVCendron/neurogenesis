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
from utils.plot_styles import cell_colors


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

g = list(sorted(list(data.keys())))
groups = g
# groups = np.concatenate((g[1:], g[0:1]))
# print(groups)

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

  fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
  # fig, ax = plt.subplots()

  # ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  ax.xaxis.set_major_formatter(formatter)
  # ax.set_ylim(0, max(max(y) for y in sds)+0.1)
  ax.set_ylim(0, 6.5)

  plt.axhline(y=1, color='gray', linestyle='--')

  cmap = LinearSegmentedColormap.from_list('neuro_cmap', [cell_colors['igc'], cell_colors['mgc']])

  groups_to_skip = ['neurogenesis_0.1_ca3', 'neurogenesis_0.3_ca3', 'neurogenesis_0.4_ca3', 'neurogenesis_0.5_ca3', 'neurogenesis_0.6_ca3', 'neurogenesis_0.7_ca3', 'neurogenesis_0.8_ca3', 'neurogenesis_0.9_ca3']
  # groups_to_skip = []
  # total_ng = len(groups) - len(groups_to_skip) - 1
  total_ng = len(groups)
  cmap_index = 0
  # values = zip(in_sims, sds, std_errors)
  for i, (in_sim, sd, std_error) in enumerate(zip(in_sims, sds, std_errors)):
    group = groups[i]
    # if group in groups_to_skip:
    #   alpha = 0.1
      # continue
    if 'control' in group:
      color = cell_colors['control']
      alpha = 0.9
    else:
      # ng_index = float(group.split('_')[1])
      # color = cmap((ng_index - 0.1) / 0.9)
      i = cmap_index / (total_ng-1)
      color = cmap(i)
      cmap_index += 1
      alpha = 0.8
      if group in groups_to_skip:
        alpha = 0.05

    label = 'Controle' if 'control' in group else f'Neurogênese: {int(float(group.split("_")[1])*100)}% de conectividade'
    label = label if not group in groups_to_skip else None
    plt.plot(in_sim, sd, color=color, alpha=alpha, label=label)

    sd_arr = np.array(sd)
    std_error_arr = np.array(std_error)
    ax.fill_between(in_sim, sd_arr - std_error_arr, sd_arr + std_error_arr, color=color, alpha=0.2)

    # plotline, caps, barlinecols = ax.errorbar(
    #     in_sim,
    #     sd,
    #     yerr=std_error,
    #     ecolor=color,
    #     linestyle='None',
    # )
    # plt.setp(barlinecols[0], capstyle="round")
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
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)

  plt.xticks(ticks=np.arange(0.1, 1.1, 0.1))

  plt.xlabel('Similaridade de entrada (%)')
  plt.ylabel('Grau de separação de padrões ($\\mathcal{S}_D$)')
  plt.legend(frameon=False)

  plt.tight_layout()
  # plt.show()
  plt.savefig(f'figures/plots/pattern_separation.jpg', dpi=300, format='jpg')
  plt.savefig(f'figures/plots/pattern_separation.pdf', format='pdf')
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
