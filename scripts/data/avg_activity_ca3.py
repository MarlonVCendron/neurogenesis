import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap

from utils.patterns import activation_degree
from utils.data import load_pattern_data
from utils.plot_styles import cell_colors

plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],

    "lines.linewidth": 6,
    'lines.solid_joinstyle': 'round',
    'lines.solid_capstyle': 'round',
})

data = load_pattern_data('teste_março')

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

  fig, ax = plt.subplots(figsize=(6, 6), dpi=300)

  ax.yaxis.set_major_locator(MaxNLocator(nbins=15))
  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  ax.yaxis.set_major_formatter(formatter)

  cads = [cads[group] for group in groups]
  std_errors_c = [std_errors_c[group] for group in groups]

  ng_groups = groups[0:]

  alpha = 0.8
  cads_arr = np.array(cads[0:])
  sems_arr = np.array(std_errors_c[0:])
  x_idx = range(len(ng_groups))

  ax.plot(x_idx, cads_arr, color=cell_colors['pca3'], label='pCA3 pattern', marker='', alpha=alpha)
  ax.fill_between(x_idx, cads_arr - sems_arr, cads_arr + sems_arr, color=cell_colors['pca3'], alpha=0.2)

  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)

  ax.legend(frameon=False)

  plt.ylabel('Ativação média da população (%)')
  plt.xlabel('Conectividade (%)')

  xlabels = range(10, 101, 10)
  plt.xticks(ticks=range(len(xlabels)), labels=xlabels)

  plt.tight_layout()
  # plt.show()
  plt.savefig(f'figures/plots/avg_activity_ca3.jpg', dpi=300, format='jpg', bbox_inches='tight')
  plt.close()


avg_activity_ca3()