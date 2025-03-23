import numpy as np
import matplotlib.pyplot as plt
from brian2 import *
import numpy as np

from params import break_time, stim_time
from utils.patterns import get_population_pattern

directory = "/home/marlon/edu/mestrado/proj/Chavlis_Hippocampus_2017/3dendrites/"
files = [
    'basket_pattern3d_1.npy',
    'hipp_pattern3d_1.npy',
    'mossy_pattern3d_1.npy',
    'input_pattern3d_1.npy',
    'output_pattern3d_1.npy',
]

data = []
for file in files:
  file_path = directory + file
  loaded_data = np.load(file_path, allow_pickle=True)
  data.append(loaded_data)

def name(file):
  return file.split('_')[0]

sim_time = 500 * ms
for idx, s in enumerate(data):
  neuron = name(files[idx])
  active = s[s>0]
  total_spikes = np.sum(s)
  firing_rate = (total_spikes / len(active)) / sim_time
  print(f'{neuron} firing rate: {firing_rate}')

plt.figure(figsize=(10, len(data) * 3))

for idx, spike_mon in enumerate(data):
  neuron = name(files[0])

  ax1 = plt.subplot(len(data), 1, idx + 1)

  ax1.plot(spike_mon, 'ok', markersize=1)
  ax1.set_xlabel('Time (ms)')
  ax1.set_ylabel(f'{neuron} index')
#   ax1.set_xlim(break_time / ms, stim_time / ms)
#   ax1.set_ylim(0, len(neuron))
plt.show()
