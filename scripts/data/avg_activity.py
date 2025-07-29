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

data = load_pattern_data('run_projeto_banca_final')

groups = sorted(list(data.keys()))


def in_similarity():
  group_stats = {}
  ads = {}
  iads = {}
  mads = {}
  std_errors = {}
  std_errors_i = {}
  std_errors_m = {}

  group_ads = {}
  group_iads = {}
  group_mads = {}

  for group in groups:
    trial_means_list = []
    in_sim_dict = {}
    i_in_sim_dict = {}
    m_in_sim_dict = {}
    for trial in data[group]:
      for pattern in trial['patterns'][:-1]:
        sim = pattern['in_similarity']
        out = pattern['gc_pattern']
        iout = pattern['igc_pattern']
        mout = pattern['mgc_pattern']

        ad = activation_degree(out)
        iad = activation_degree(iout)
        mad = activation_degree(mout)

        if sim not in in_sim_dict:
          in_sim_dict[sim] = []
        in_sim_dict[sim].append(ad)

        if sim not in i_in_sim_dict:
          i_in_sim_dict[sim] = []
        i_in_sim_dict[sim].append(iad)

        if sim not in m_in_sim_dict:
          m_in_sim_dict[sim] = []
        m_in_sim_dict[sim].append(mad)

        if group not in group_ads:
          group_ads[group] = []
        if group not in group_iads:
          group_iads[group] = []
        if group not in group_mads:
          group_mads[group] = []
        group_ads[group].append(ad)
        group_iads[group].append(iad)
        group_mads[group].append(mad)

    mean_ad = np.mean([np.mean(ads) for ads in in_sim_dict.values()])
    mean_iad = np.mean([np.mean(ads) for ads in i_in_sim_dict.values()])
    mean_mad = np.mean([np.mean(ads) for ads in m_in_sim_dict.values()])

    std_error_ad = sem([np.mean(ads) for ads in in_sim_dict.values()])
    std_error_iad = sem([np.mean(ads) for ads in i_in_sim_dict.values()])
    std_error_mad = sem([np.mean(ads) for ads in m_in_sim_dict.values()])

    ads[group] = mean_ad
    iads[group] = mean_iad
    mads[group] = mean_mad

    std_errors[group] = std_error_ad
    std_errors_i[group] = std_error_iad
    std_errors_m[group] = std_error_mad

  fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
  # fig, ax = plt.subplots()

  cmap = LinearSegmentedColormap.from_list('neuro_cmap', ["#16a4d8", '#8bd346'])

  # ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
  ax.yaxis.set_major_locator(MaxNLocator(nbins=15))
  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  ax.yaxis.set_major_formatter(formatter)


  ads = [ads[group] for group in groups]
  iads = [iads[group] for group in groups]
  mads = [mads[group] for group in groups]

  std_errors = np.array([std_errors[group] for group in groups])
  std_errors_i = [std_errors_i[group] for group in groups]
  std_errors_m = [std_errors_m[group] for group in groups]

  # ax.axhline(y=ads[0], color=c_color, linestyle='--')
  ax.axhline(y=ads[0], color=cell_colors['control'], linestyle='--')

  ng_groups = groups[1:]
  
  alpha = 0.8
  ax.plot(ng_groups, ads[1:], color=cell_colors['gc'], label='Full GC population pattern', marker='', alpha=alpha)
  ax.plot(ng_groups, iads[1:], color=cell_colors['igc'], label='iGC pattern', marker='', alpha=alpha)
  ax.plot(ng_groups, mads[1:], color=cell_colors['mgc'], label='mGC pattern', marker='', alpha=alpha)

  _,_,barlinecols = ax.errorbar(
      ng_groups,
      ads[1:],
      yerr=std_errors[1:],
      ecolor=cell_colors['gc'],
      linestyle='None'
  )
  plt.setp(barlinecols[0], capstyle="round")

  _,_,barlinecols = ax.errorbar(
      ng_groups,
      iads[1:],
      yerr=std_errors_i[1:],
      ecolor=cell_colors['igc'],
      linestyle='None'
  )
  plt.setp(barlinecols[0], capstyle="round")
  
  _,_,barlinecols = ax.errorbar(
      ng_groups,
      mads[1:],
      yerr=std_errors_m[1:],
      ecolor=cell_colors['mgc'],
      linestyle='None'
  )
  plt.setp(barlinecols[0], capstyle="round")
      

  ax.legend(frameon=False)

  sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.1, vmax=1.0))
  sm.set_array([])

  plt.ylabel('Ativação média da população (%)')
  plt.xlabel('Conectividade (%)')

  xlabels = range(10, 101, 10)
  # xlabels = np.array(xlabels) / 100
  plt.xticks(ticks=range(len(xlabels)), labels=xlabels)

  plt.tight_layout()
  # plt.show()
  plt.savefig(f'figures/plots/avg_activity.jpg', dpi=300, format='jpg')
  plt.close()

  # print(f'full: min: {np.min(ads[1:])}, max: {np.max(ads[1:])}')
  # print(f'iGCs: min: {np.min(iads[1:])}, max: {np.max(iads[1:])}')
  # print(f'mGCs: min: {np.min(mads[1:])}, max: {np.max(mads[1:])}')

  # for group in groups:
  #   if (group == 'control'):
  #     continue

  #   t_stat, p_value = ttest_ind(
  #       group_ads['control'],
  #       group_ads[group],
  #       equal_var=False  # Welch's t-test (doesn't assume equal variance)
  #   )
  #   print(f"t-statistic for {group}: {t_stat}, p-value: {p_value} {'**' if p_value < 0.05 else ''}")


in_similarity()