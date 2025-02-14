from brian2 import *
from neurogenesis.utils.connect import Connect
from neurogenesis.params import syn_params 
from neurogenesis.params.cells import cell_params
from neurogenesis.models.cells import (
    create_mgc,
    create_igc,
    create_bc,
    create_mc,
    create_hipp,
    create_ec,
)

seed(1)

defaultclock.dt = 0.1 * ms

def to_100(params):
  return {**params, "p": 1.0}

def main():
  start_scope()

  # ec  = create_ec(N=2, active_p=1.0, rate=20*Hz)
  mgc = create_mgc(N=1)
  bc  = create_ec(N=2, active_p=1.0, rate=1000*Hz, name='bc')

  bc_gaba_mgc = Connect(bc, mgc, **to_100(syn_params['bc_gaba_mgc']))

  print('Created connections')

  # mon = StateMonitor(bc, 'Vm', record=True)
  mon = StateMonitor(mgc, True, record=True)
  mon_syn_ec = StateMonitor(bc_gaba_mgc, 'g_syn', record=True)

  neurons = [mgc, bc]
  labels = [neuron.name for neuron in neurons]
  spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]

  net = Network(collect())
  net.add(spike_monitors)

  print('Running simulation')
  net.run(200*ms)

  # plt.plot(mon.t / ms, mon.Vm[0] / mV)
  plt.subplot(2, 1, 1)
  plt.plot(mon.t / ms, mon.Vm[0] / mV, alpha=0.5) 
  plt.subplot(2, 1, 2)
  plt.plot(mon_syn_ec.t / ms, mon_syn_ec.g_syn[0])
  # plt.plot(mon.t / ms, mon.I_ampa_2[0] / nA)
  plt.show()

  # for spike_mon in spike_monitors:
  #   print(f'Number of {labels[spike_monitors.index(spike_mon)]} that fired: {len(set(spike_mon.i))}')
 
  #   plt.subplot(len(spike_monitors), 1, spike_monitors.index(spike_mon) + 1)
  #   plt.plot(spike_mon.t / ms, spike_mon.i, '|k', markersize=1)
  #   plt.xlabel('Time (ms)')
  #   plt.ylabel(f'{labels[spike_monitors.index(spike_mon)]} index')
  # plt.show()


if __name__ == '__main__':
  main()

