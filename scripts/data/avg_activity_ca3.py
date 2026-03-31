import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from scipy.stats import ttest_ind
from scipy.interpolate import make_interp_spline



from utils.patterns import activation_degree
from utils.data import load_pattern_data
from utils.plot_styles import cell_colors

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

  fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
  # fig, ax = plt.subplots()

  cmap = LinearSegmentedColormap.from_list('neuro_cmap', ["#16a4d8", '#8bd346'])

  # ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
  ax.yaxis.set_major_locator(MaxNLocator(nbins=15))
  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  ax.yaxis.set_major_formatter(formatter)


  cads = [cads[group] for group in groups]

  std_errors_c = [std_errors_c[group] for group in groups]

  # ax.axhline(y=ads[0], color=c_color, linestyle='--')
  # ax.axhline(y=ads[0], color=cell_colors['control'], linestyle='--')

  ng_groups = groups[0:]
  
  alpha = 0.8
  ax.plot(ng_groups, cads[0:], color=cell_colors['pca3'], label='pCA3 pattern', marker='', alpha=alpha)

  _,_,barlinecols = ax.errorbar(
      ng_groups,
      cads[0:],
      yerr=std_errors_c[0:],
      ecolor=cell_colors['pca3'],
      linestyle='None'
  )
  plt.setp(barlinecols[0], capstyle="round")
   
      

  ax.legend(frameon=False)

  sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.1, vmax=1.0))
  sm.set_array([])

  plt.ylabel('Ativação média da população (%)')
  plt.xlabel('Conectividade (%)')

  # xlabels = range(10, 101, 10)
  xlabels = range(10, 31, 10)
  # xlabels = np.array(xlabels) / 100
  plt.xticks(ticks=range(len(xlabels)), labels=xlabels)

  plt.tight_layout()
  # plt.show()
  plt.savefig(f'figures/plots/avg_activity_ca3.jpg', dpi=300, format='jpg')
  plt.close()


avg_activity_ca3()