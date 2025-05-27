from brian2 import *
from utils.connect import Connect
from params import syn_params 
from params.cells import cell_params
from plotting.voltage import plot_voltage
from models.general import AdEx

seed(1)

defaultclock.dt = 0.1 * ms

def to_100(params):
  return {**params, "p": 1.0}

def main():
  start_scope()

  adex_eqs, threshold, reset, refractory = AdEx()

  neuron = NeuronGroup(
      N          = 1,
      model      = adex_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      name       = 'adex',
      method     = 'rk2',
  )

  # Params
  neuron.Cm        = 281 * pF
  neuron.g_L       = 30 * nS
  neuron.E_L       = -70.6 * mV
  neuron.V_th      = -50.4 * mV
  neuron.DeltaT    = 2 * mV
  neuron.tau_o     = 144 * ms
  neuron.a         = 4 * nS
  neuron.b         = 0.0805 * nA
  neuron.V_reset   = -56.0 * mV
  neuron.eta       = 0.28 * mM**-1
  neuron.gamma     = 0.072 * mV**-1
  neuron.Mg_conc   = 1 * mM

  # Initialize
  neuron.Vm = neuron.E_L

  spike_monitor = SpikeMonitor(neuron)
  state_monitor = StateMonitor(neuron, ['Vm', 'I_exp', 'o'], record=True)

  net = Network(collect())
  net.add(spike_monitor)
  net.add(state_monitor)

  print('Running simulation')
  # duration = 300 * ms
  # net.run(duration)

  # baseline = 0.34 * nA
  # neuron.I_ext = baseline
  # net.run(200 * ms)
  # for i in range(5):
  #   neuron.I_ext = 2 * nA + baseline
  #   net.run(5 * ms)
  #   # neuron.I_ext = 0 * nA
  #   neuron.I_ext = baseline
  #   net.run(95 * ms)

  neuron.I_ext = 0.0 * nA
  net.run(10 * ms)

  neuron.I_ext = 0.5 * nA
  net.run(190 * ms)

  neuron.I_ext = 0.0 * nA
  net.run(300 * ms)

  neuron.I_ext = 0.75 * nA
  net.run(500 * ms)

  neuron.I_ext = 0.0 * nA
  net.run(200 * ms)
  
  print(f'Spike count: {spike_monitor.count}')
  
  # plt.plot(state_monitor.t / ms, state_monitor.Vm[0] / mV)
  # plt.show()

  plot_voltage(state_monitor, spike_monitor)

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

