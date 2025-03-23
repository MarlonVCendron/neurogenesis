import numpy as np
import matplotlib.pyplot as plt
from brian2 import *
import numpy as np

from params import break_time, stim_time
from utils.patterns import get_population_pattern


directory = "/home/marlon/edu/mestrado/proj/in-vivo-brian2/results/Control/"
# files = [
#     'hipp_pattern.npy',
#     'input_pattern.npy',
#     'output_pattern.npy',
# ]
files = [
    'hipp_spikes.npy',
    'input_spikes.npy',
    'output_spikes.npy',
]



data = []
for file in files:
  file_path = directory + file
  loaded_data = np.load(file_path, allow_pickle=True, encoding='latin1')
  data.append(loaded_data)

def get_name(file):
  return file.split('_')[0]

sim_time = 610 * ms
# for idx, s in enumerate(data):
#   neuron = name(files[idx])
#   active = s[s>0]
#   total_spikes = np.sum(s)
#   firing_rate = (total_spikes / len(active)) / sim_time
#   print(f'{neuron} firing rate: {firing_rate}')

plt.figure(figsize=(10, len(data) * 3))

# for idx, spike_mon in enumerate(data):
#   neuron = name(files[idx])

#   ax1 = plt.subplot(len(data), 1, idx + 1)

#   ax1.plot(spike_mon, 'ok', markersize=1)
#   ax1.set_xlabel('Time (ms)')
#   ax1.set_ylabel(f'{neuron} index')
# #   ax1.set_xlim(break_time / ms, stim_time / ms)
# #   ax1.set_ylim(0, len(neuron))


for idx, spike_mon in enumerate(data):
  name = get_name(files[idx])

  ax1 = plt.subplot(len(data), 1, idx + 1)

  t = []
  i = []
  for idx, neuron in enumerate(spike_mon):
    n_spikes = len(neuron)
    t.extend(neuron*1000)
    i.extend([idx] * n_spikes)

  total_active = len(i)
  print(f'{name} total: {total_active}')
  
  ax1.plot(t, i, 'ok', markersize=1)
  ax1.set_xlabel('Time (ms)')
  ax1.set_ylabel(f'{name} index')
  ax1.set_xlim(0, sim_time / ms)
#   ax1.set_ylim(0, len(neuron))

plt.show()
