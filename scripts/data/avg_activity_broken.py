import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap



from utils.patterns import activation_degree
from utils.data import load_pattern_data
from utils.plot_styles import cell_colors, dense_dots

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

  # fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
  fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 1]}, figsize=(6, 6), dpi=300)
  fig.subplots_adjust(hspace=0.05)


  # fig, ax = plt.subplots()

  # ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
  formatter = FuncFormatter(lambda y, _: f'{y*100:.0f}')
  for axis in [ax, ax2]:
    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_major_formatter(formatter)


  ads = [ads[group] for group in groups]
  iads = [iads[group] for group in groups]
  mads = [mads[group] for group in groups]

  std_errors = np.array([std_errors[group] for group in groups])
  std_errors_i = [std_errors_i[group] for group in groups]
  std_errors_m = [std_errors_m[group] for group in groups]

  for axis in [ax, ax2]:
    axis.axhline(y=ads[0], color=cell_colors['control'], linestyle='--', label='Controle')

  ng_groups = groups[1:]
  
  alpha = 0.8

  ads_data = np.array(ads[1:])
  iads_data = np.array(iads[1:])
  mads_data = np.array(mads[1:])
  std_errors_data = np.array(std_errors[1:])
  std_errors_i_data = np.array(std_errors_i[1:])
  std_errors_m_data = np.array(std_errors_m[1:])

  for axis in [ax, ax2]:
    axis.plot(ng_groups, ads_data, color=cell_colors['gc'], label='Total GC', marker='', alpha=alpha)
    axis.plot(ng_groups, iads_data, color=cell_colors['igc'], label='iGC', marker='', alpha=alpha, linestyle=dense_dots)
    axis.plot(ng_groups, mads_data, color=cell_colors['mgc'], label='mGC', marker='', alpha=alpha, linestyle=dense_dots)

    axis.fill_between(ng_groups, ads_data - std_errors_data, ads_data + std_errors_data, color=cell_colors['gc'], alpha=0.2)
    axis.fill_between(ng_groups, iads_data - std_errors_i_data, iads_data + std_errors_i_data, color=cell_colors['igc'], alpha=0.2)
    axis.fill_between(ng_groups, mads_data - std_errors_m_data, mads_data + std_errors_m_data, color=cell_colors['mgc'], alpha=0.2)
      
  all_ys = np.concatenate([ads_data, iads_data, mads_data])
  y_with_error_min = np.concatenate([
      ads_data - std_errors_data,
      iads_data - std_errors_i_data,
      mads_data - std_errors_m_data
  ])
  y_with_error_max = np.concatenate([
      ads_data + std_errors_data,
      iads_data + std_errors_i_data,
      mads_data + std_errors_m_data
  ])
  
  min_val = np.min(y_with_error_min)
  max_val = np.max(y_with_error_max)

  ax.set_ylim(.17, max_val * 1.05)
  ax2.set_ylim(min_val * .95, .16)

  ax.spines['bottom'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  ax2.spines['top'].set_visible(False)
  ax2.spines['right'].set_visible(False)
  # ax.xaxis.tick_top()
  # ax.tick_params(labeltop=False)
  ax.xaxis.set_visible(False)
  ax2.xaxis.tick_bottom()

  d = .015
  kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
  ax.plot((-d, +d), (-d, +d), **kwargs)
  # ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)

  kwargs.update(transform=ax2.transAxes)
  ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)
  # ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

  # for i, group in enumerate(ng_groups):
  #   t_stat, p_value = ttest_ind(
  #       group_ads['control_ca3'],
  #       group_ads[group],
  #       equal_var=False  # Welch's t-test (doesn't assume equal variance)
  #   )

  #   if p_value < 0.001:
  #     y_value = ads[i+1] + std_errors[i+1]
  #     ax.text(i, y_value + 0.002, '*', ha='center', va='bottom', color='black', fontsize=20, fontweight='bold')

  ax.legend(frameon=False)

  fig.supylabel('Ativação média da população (%)', fontsize=18)
  plt.xlabel('Conectividade (%)')

  xlabels = range(10, 101, 10)
  # xlabels = np.array(xlabels) / 100
  plt.xticks(ticks=range(len(xlabels)), labels=xlabels)

  plt.tight_layout()
  # plt.show()
  plt.savefig(f'figures/plots/avg_activity.jpg', dpi=300, format='jpg')
  plt.savefig(f'figures/plots/avg_activity.pdf', format='pdf')
  plt.close()


in_similarity()
