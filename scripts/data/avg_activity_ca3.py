import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap

from utils.patterns import activation_degree
from utils.data import load_pattern_data
from utils.plot_styles import cell_colors, alpha, linewidth, igc_connectivity_label

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],

    "lines.linewidth": linewidth,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

data = load_pattern_data('april_2026')

groups = sorted(list(data.keys()))


def avg_activity_ca3():
  cads = {}
  std_errors_c = {}

  group_cads = {}

  for group in groups:
    c_in_sim_dict = {}
    for trial in data[group]:
      for pattern in trial['patterns'][:-1]:
        sim = pattern['in_similarity']
        cout = pattern['pca3_pattern']

        cad = activation_degree(cout)

        if sim not in c_in_sim_dict:
          c_in_sim_dict[sim] = []
        c_in_sim_dict[sim].append(cad)

        if group not in group_cads:
          group_cads[group] = []

        group_cads[group].append(cad)

    mean_cad = np.mean([np.mean(ads) for ads in c_in_sim_dict.values()])

    std_error_cad = sem([np.mean(ads) for ads in c_in_sim_dict.values()])

    cads[group] = mean_cad

    std_errors_c[group] = std_error_cad

  fig, ax = plt.subplots(figsize=(6, 4), dpi=300)

  from matplotlib.ticker import MultipleLocator
  ax.yaxis.set_major_locator(MultipleLocator(0.03))
  formatter = FuncFormatter(lambda y, _: f'{round(y*100)}')
  ax.yaxis.set_major_formatter(formatter)
  print(cads)

  cads = [cads[group] for group in groups]
  std_errors_c = [std_errors_c[group] for group in groups]

  ng_groups = groups[1:]

  cads_arr = np.array(cads[1:])
  sems_arr = np.array(std_errors_c[1:])
  x_idx = range(len(ng_groups))

  ax.axhline(y=cads[0], color=cell_colors['control'], linestyle='--', label='Control')

  ax.plot(x_idx, cads_arr, color=cell_colors['pca3'], label='pCA3', marker='', alpha=alpha)
  ax.fill_between(x_idx, cads_arr - sems_arr, cads_arr + sems_arr, color=cell_colors['pca3'], alpha=0.2)

  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)

  max_val = np.max(cads_arr)
  min_val = np.min(cads_arr)
  pad = 0.2
  ax.set_ylim((1-pad) * min_val, (1+pad) * max_val)

  ax.legend(frameon=False)

  plt.ylabel('Mean population activation (%)')
  plt.xlabel(igc_connectivity_label)

  xlabels = range(10, 101, 10)
  plt.xticks(ticks=range(len(xlabels)), labels=[10, '', '', 40, '', '', 70, '', '', 100])

  plt.tight_layout()
  # plt.show()
  plt.savefig(f'figures/plots/avg_activity_ca3.jpg', dpi=300, format='jpg', bbox_inches='tight')
  plt.close()


avg_activity_ca3()