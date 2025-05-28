from brian2 import *

def plot_voltage(monitor, spike_monitor, idx=0):
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot as plt

  neuron = monitor.source
  states = neuron.get_states()
  if 'V_th' in states:
    threshold = states['V_th'][idx]
  elif 'Vt' in states:
    threshold = states['Vt'][idx]
  else:
    print("Warning: Threshold potential (V_th or Vt) not found in neuron states.")
    threshold = 0 * mV 

  all_spikes = spike_monitor.all_values()

  plt.plot(monitor.t / ms, monitor.Vm[idx] / mV, color="black")
  for spike_time in all_spikes['t'][idx] / ms:
    plt.plot([spike_time, spike_time], [threshold / mV, 20], color="black")
  plt.xticks(rotation=45)
  plt.locator_params(axis="x", nbins=60)
  plt.grid(True, which="both", linestyle="--", alpha=0.2)
  plt.xlabel('Time (ms)')
  plt.ylabel('Voltage (mV)')

  plt.show()
  # plt.savefig(f'figures/voltage_{num}.png')
  # plt.close()