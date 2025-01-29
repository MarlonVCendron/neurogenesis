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

def main():
  start_scope()

  (ec, _) = create_ec(N=1, active_p=1.0, rate=100*Hz)
  mgc     = create_mgc(N=1)

  # remove p from object
  syn_ampa = {**syn_params['ec_ampa_mgc'], 'p': 1.0}
  syn_nmda = {**syn_params['ec_nmda_mgc'], 'p': 1.0}
  syn_gaba = {**syn_params['bc_gaba_mgc'], 'p': 1.0}
  # ec_ampa_mgc = Connect(ec, mgc, **syn_ampa)
  # ec_nmda_mgc = Connect(ec, mgc, **syn_nmda)
  gaba = Connect(ec, mgc, **syn_gaba)


  print('Created connections')

  mon = StateMonitor(mgc, 'I_gaba', record=True)
  # mon_syn = StateMonitor(ec_ampa_mgc, 'g', record=True)
  # mon_syn = StateMonitor(ec_nmda_mgc, 'g', record=True)
  # mon_syn = StateMonitor(gaba, 'I_synapse', record=True)

  neurons = [ec, mgc]
  labels = [neuron.name for neuron in neurons]
  spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]

  net = Network(collect())
  net.add(spike_monitors)

  print('Running simulation')
  net.run(20*ms)

  plt.plot(mon.t / ms, mon.I_gaba[0] / mV)
  # plt.plot(mon_syn.t / ms, mon_syn.g[0])
  plt.show()

  # for spike_mon in spike_monitors:
  #   print(f'Number of {labels[spike_monitors.index(spike_mon)]} that fired: {len(set(spike_mon.i))}')
 
  #   plt.subplot(len(spike_monitors), 1, spike_monitors.index(spike_mon) + 1)
  #   plt.plot(spike_mon.t / ms, spike_mon.i, '|k')
  #   plt.xlabel('Time (ms)')
  #   plt.ylabel(f'{labels[spike_monitors.index(spike_mon)]} index')
  # plt.show()


if __name__ == '__main__':
  main()

