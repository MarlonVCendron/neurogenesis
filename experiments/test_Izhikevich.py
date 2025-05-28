from brian2 import *
from utils.connect import Connect
from params import syn_params 
from params.cells import cell_params
from plotting.voltage import plot_voltage
from utils.create_neuron_group import create_neuron_group

seed(1)

defaultclock.dt = 0.1 * ms

def to_100(params):
  return {**params, "p": 1.0}

def main():
  start_scope()

  # neuron = create_neuron_group(
  #     N          = 1,
  #     model      = 'izhikevich',
  #     k          = 0.44,
  #     a          = 0.003,
  #     b          = 24.4,
  #     d          = 50,
  #     Cm         = 38 * pF,
  #     Vr         = -77.4 * mV,
  #     Vt       = -44.9 * mV,
  #     Vpeak      = 15.49 * mV,
  #     Vmin     = -66.46 * mV,
  #     name       = 'izhikevich_neuron',
  #     refractory = 0 * ms
  # )

  neuron = create_neuron_group(
      N     = 1,
      model = 'izhikevich',
      k     = 0.4471817006977834,
      a     = 0.0032799410036917333,
      b     = 24.478421990208606,
      d     = 50,
      Cm    = 38 * pF,
      Vr    = -77.40291336465064 * mV,
      Vt  = -44.90054428048817 * mV,
      Vpeak = 15.489726771001997 * mV,
      Vmin  = -66.46563513097735 * mV,
      name  = 'izhikevich_neuron',
  )

  neuron.Vm = 0 * mV

  spike_monitor = SpikeMonitor(neuron)
  state_monitor = StateMonitor(neuron, ['Vm', 'u'], record=True)

  net = Network(collect())
  net.add(spike_monitor)
  net.add(state_monitor)

  print('Running simulation')

  neuron.I_ext = 0.0 * nA
  net.run(20 * ms)

  neuron.I_ext = 0.5 * nA
  net.run(80 * ms)

  neuron.I_ext = 0.0 * nA
  net.run(100 * ms)

  # neuron.I_ext = 0.75 * nA
  # net.run(500 * ms)

  # neuron.I_ext = 0.0 * nA
  # net.run(200 * ms)
  
  print(f'Spike count: {spike_monitor.count}')
  
  # plot_voltage(state_monitor, spike_monitor)

  # all_spikes = spike_monitor.all_values()
  # for spike_time in all_spikes['t'][0] / ms:
  #   plt.plot([spike_time, spike_time], [30, 35], color="black")

  plt.plot(state_monitor.t / ms, state_monitor.Vm[0] / mV)
  plt.show()

  # plt.plot(state_monitor.t / ms, state_monitor.I_exp[0] / nA)
  # plt.show()

  # plt.plot(state_monitor.t / ms, state_monitor.w[0] / nA)
  # plt.show()

  # for I in np.arange(0, 1.2, 0.1) * nA:
  #   neuron.I_ext = I
  #   net.run(1 * second)
  #   print(f'I_ext: {I}, spike count: {spike_monitor.count}')




if __name__ == '__main__':
  main()

