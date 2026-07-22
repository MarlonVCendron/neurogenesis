import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FuncFormatter
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

from utils.patterns import pattern_separation_degree
from utils.data import load_pattern_data
from scipy.stats import mannwhitneyu
import itertools
from utils.plot_styles import cell_colors, linewidth


plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],

    "lines.linewidth": linewidth,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

data = load_pattern_data('june_final')

g = list(sorted(list(data.keys())))
groups = g


def count_vector(pattern, cell_type, fallback_key):
  counts = pattern.get('spike_counts', {})
  vec = counts.get(cell_type, pattern[fallback_key])
  return np.asarray(vec, dtype=float)


def separation_curve(group, use_counts, out_type='mgc', out_fallback='mgc_pattern'):
  in_sim_dict = {}
  for trial in data[group]:
    original_pattern = trial['original_pattern']
    if use_counts:
      original_inp = count_vector(original_pattern, 'pp', 'pp_pattern')
      original_out = count_vector(original_pattern, out_type, out_fallback)
    else:
      original_inp = np.asarray(original_pattern['pp_pattern'])
      original_out = np.asarray(original_pattern[out_fallback])

    for pattern in trial['patterns'][:-1]:
      sim = pattern['in_similarity']
      if use_counts:
        inp = count_vector(pattern, 'pp', 'pp_pattern')
        out = count_vector(pattern, out_type, out_fallback)
      else:
        inp = np.asarray(pattern['pp_pattern'])
        out = np.asarray(pattern[out_fallback])

      if np.array(original_out).shape != np.array(out).shape:
        continue

      s_d = pattern_separation_degree(original_inp, inp, original_out, out)
      if s_d != float("inf") and not np.isnan(s_d):
        in_sim_dict.setdefault(sim, []).append(s_d)

  return {sim: float(np.mean(vals)) for sim, vals in sorted(in_sim_dict.items())}


def count_vs_binary_correlation(out_type='mgc', out_fallback='mgc_pattern'):
  corrs = []
  for group in groups:
    binary_curve = separation_curve(group, False, out_type, out_fallback)
    count_curve = separation_curve(group, True, out_type, out_fallback)
    sims = sorted(set(binary_curve) & set(count_curve))
    binary_vals = [binary_curve[sim] for sim in sims]
    count_vals = [count_curve[sim] for sim in sims]
    if len(sims) >= 2 and np.std(binary_vals) > 0 and np.std(count_vals) > 0:
      r = np.corrcoef(binary_vals, count_vals)[0, 1]
      corrs.append(r)
      print(f'{group}: r = {r:.4f}')
  if corrs:
    print(f'mean r (binary vs count) = {np.mean(corrs):.4f} '
          f'[min {np.min(corrs):.4f}, max {np.max(corrs):.4f}]')


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
      original_inp = count_vector(original_pattern, 'pp', 'pp_pattern')
      original_out = count_vector(original_pattern, 'mgc', 'mgc_pattern')

      for pattern in trial['patterns'][:-1]:
        sim = pattern['in_similarity']
        inp = count_vector(pattern, 'pp', 'pp_pattern')
        out = count_vector(pattern, 'mgc', 'mgc_pattern')

        if np.array(original_out).shape != np.array(out).shape:
          continue

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

  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  ax.xaxis.set_major_formatter(formatter)

  plt.axhline(y=1, color='gray', linestyle='--')

  cmap = LinearSegmentedColormap.from_list('neuro_cmap', [cell_colors['igc'], cell_colors['mgc']])

  groups_to_skip = ['neurogenesis_0.1_ca3', 'neurogenesis_0.3_ca3', 'neurogenesis_0.4_ca3', 'neurogenesis_0.6_ca3', 'neurogenesis_0.7_ca3', 'neurogenesis_0.8_ca3', 'neurogenesis_0.9_ca3']
  total_ng = len(groups)
  cmap_index = 0
  for i, (in_sim, sd, std_error) in enumerate(zip(in_sims, sds, std_errors)):
    group = groups[i]
    if 'control' in group:
      color = cell_colors['control']
      linestyle='--'
      alpha = 0.9
    else:
      i = cmap_index / (total_ng-1)
      color = cmap(i)
      cmap_index += 1
      alpha = 0.9
      linestyle='-'
      if group in groups_to_skip:
        alpha = 0

    label = 'Control' if 'control' in group else f'Neurogenesis: {int(float(group.split("_")[1])*100)}% excitability'
    label = label if not group in groups_to_skip else None
    plt.plot(in_sim, sd, color=color, alpha=alpha, label=label, linestyle=linestyle)

    sd_arr = np.array(sd)
    std_error_arr = np.array(std_error)
    ax.fill_between(in_sim, sd_arr - std_error_arr, sd_arr + std_error_arr, color=color, alpha=alpha*0.2)

  # ax.spines['right'].set_visible(False)
  # ax.spines['top'].set_visible(False)

  # plt.xticks(ticks=np.arange(0.1, 1, 0.1))

  # plt.xlabel('Input similarity (%)')
  # plt.ylabel('Pattern separation degree ($\\mathcal{S}_D$)')
  # plt.legend(frameon=False)

  # plt.tight_layout()
  # plt.savefig(f'figures/plots/pattern_separation_count.jpg', dpi=300, format='jpg')
  # plt.savefig(f'figures/plots/pattern_separation_count.pdf', format='pdf')
  # plt.close()


# in_similarity()
print('mGC population:')
count_vs_binary_correlation('mgc', 'mgc_pattern')
print()
print('pCA3 population:')
count_vs_binary_correlation('pca3', 'pca3_pattern')
