import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import sem
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

from utils.patterns import pattern_separation_degree, pattern_integration_degree, activation_degree, correlation_degree
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

g = list(sorted(list(data.keys())))
groups = np.concatenate((g[1:], g[0:1])) 

def in_similarity():
  in_sims = []
  sds = []
  std_devs = []
  for group in groups:
    in_sim_dict = {}
    for trial in data[group]:
      # for trial in data['control']:
      original_pattern = trial['original_pattern']
      # if original_pattern == None:
      #   continue
      
      original_inp = original_pattern['pp_pattern']
      original_out = original_pattern['gc_pattern']

      for pattern in trial['patterns'][:-1]:
        sim = pattern['in_similarity']
        inp = pattern['pp_pattern']
        out = pattern['gc_pattern']
        s_d = pattern_separation_degree(original_inp, inp, original_out, out)
        # s_d = activation_degree(out)
        # s_d = activation_degree(inp)
        # s_d = correlation_degree(original_inp, inp)
        # s_d = correlation_degree(original_out, out)

        if sim not in in_sim_dict:
          in_sim_dict[sim] = []
        if s_d != float("inf") and s_d != np.nan:
          in_sim_dict[sim].append(s_d)

    average_sd = {sim: np.mean(sds) for sim, sds in in_sim_dict.items()}
    # std_error = {sim: sem(sds) for sim, sds in in_sim_dict.items()}
    std_dev = {sim: np.std(sds, ddof=1) for sim, sds in in_sim_dict.items()}  # Standard Deviation (SD)


    sorted_in_sim = sorted(average_sd.keys())
    sorted_average_sd = [average_sd[sim] for sim in sorted_in_sim]
    sorted_std_dev = [std_dev[sim] for sim in sorted_in_sim]

    in_sims.append(sorted_in_sim)
    sds.append(sorted_average_sd)
    std_devs.append(sorted_std_dev)
  
  fig, ax = plt.subplots()
  ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
  ax.set_ylim(0, max(max(y) for y in sds)+0.1)

  c_color = "#d64e12"
  cmap = LinearSegmentedColormap.from_list('neuro_cmap', ["#16a4d8", '#8bd346'])


  for i, (in_sim, sd, std_dev) in enumerate(zip(in_sims, sds, std_devs)):
    group = groups[i]
    if group == 'control':
      color = c_color
      marker="o"
      alpha = 0.9
    else:
      ng_index = float(group.split('_')[1])
      color = cmap((ng_index - 0.1) / 0.9)
      marker="X"
      alpha = 0.5

    plt.plot(in_sim, sd, color=color, label=group, marker=marker, alpha=alpha)

    # ax.errorbar(
    #     in_sim,
    #     sd,
    #     yerr=std_dev,
    #     color=color
    # )

  legend_elements = [
    Line2D([0], [0], color=c_color, label='Control', marker='o'),
    Line2D([0], [0], label='Neurogenesis: 10% connectivity', marker='X', color=cmap(0)),
    Line2D([0], [0], label='Neurogenesis: 100% connectivity', marker='X', color=cmap(1.0)),
  ]
  plt.legend(handles=legend_elements, loc='upper left')
             
  
  # Add a colorbar to show the gradient scale
  sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.1, vmax=1.0))
  sm.set_array([])
  # cbar = plt.colorbar(sm, ax=plt.gca(), pad=0.1)

  plt.title('Pattern separation degree ($\\mathcal{S}_D$) by input similarity')
  plt.xlabel('Input similarity')
  plt.ylabel('$\\mathcal{S}_D$')
  plt.axhline(y=1, color='gray', linestyle='--')
  # plt.legend()

  plt.show()


in_similarity()
