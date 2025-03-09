from brian2 import *

def plot_voltage(monitor, spike_monitor):
  import matplotlib
  matplotlib.use('TkAgg')
  import matplotlib.pyplot as plt

  neuron = monitor.source
  threshold = neuron.get_states()['V_th'][0]

  plt.plot(monitor.t / ms, monitor.Vm[0] / mV, color="black")
  for spike_time in spike_monitor.t / ms:
    plt.plot([spike_time, spike_time], [threshold / mV, 20], color="black")
  plt.xticks(rotation=45)
  plt.locator_params(axis="x", nbins=60)
  plt.grid(True, which="both", linestyle="--", alpha=0.2)
  plt.xlabel('Time (ms)')
  plt.ylabel('Voltage (mV)')

  plt.show()
  # plt.savefig(f'neurogenesis/figures/voltage_{num}.png')
  # plt.close()