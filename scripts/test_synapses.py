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

  (ec, _)  = create_ec(N=1, active_p=1.0, rate=20*Hz)
  # (mgc, _) = create_ec(N=2, active_p=1.0, rate=20*Hz, name='mgc')
  # mgc     = create_mgc(N=1)
  bc      = create_bc(N=1)

  ec_ampa_bc  = Connect(ec, bc, **to_100(syn_params['ec_ampa_bc']))
  # ec_nmda_bc  = Connect(ec, bc, **to_100(syn_params['ec_nmda_bc']))

  # mgc_ampa_bc   = Connect(mgc, bc, **to_100(syn_params['mgc_ampa_bc']))
  # mgc_nmda_bc   = Connect(mgc, bc, **to_100(syn_params['mgc_nmda_bc']))

  print('Created connections')

  # mon = StateMonitor(bc, 'Vm', record=True)
  mon = StateMonitor(bc, True, record=True)
  mon_syn_ec = StateMonitor(ec_ampa_bc, 'g_syn', record=True)
  # mon_syn_mgc = StateMonitor(mgc_ampa_bc, 'g_syn', record=True)

  # neurons = [ec, mgc, bc]
  neurons = [ec, bc]
  labels = [neuron.name for neuron in neurons]
  spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]

  net = Network(collect())
  net.add(spike_monitors)

  print('Running simulation')
  net.run(30*ms)

  # plt.plot(mon.t / ms, mon.Vm[0] / mV)
  # plt.show()

  plt.plot(mon_syn_ec.t / ms, mon_syn_ec.g_syn[0] / nS)
  plt.xticks(rotation=45)
  plt.locator_params(axis="x", nbins=60)
  plt.grid(True, which="both", linestyle="--", alpha=0.2)
  plt.show()

  # plt.subplot(2, 1, 1)
  # plt.plot(mon.t / ms, -1*mon.I_ampa_1[0] / nA, alpha=0.5)
  # plt.plot(mon.t / ms, -1*mon.I_ampa_2[0] / nA, alpha=0.5)
  # plt.plot(mon.t / ms, -1*mon.I_ampa[0] / nA, alpha=0.5) 
  # plt.subplot(2, 1, 2)
  # plt.plot(mon_syn_ec.t / ms, mon_syn_ec.g_syn[0])
  # plt.plot(mon_syn_mgc.t / ms, mon_syn_mgc.g_syn[0])
  # plt.plot(mon_syn_ec.t / ms, mon_syn_ec.g_syn[1])
  # plt.plot(mon_syn_mgc.t / ms, mon_syn_mgc.g_syn[1])
  # # plt.plot(mon.t / ms, mon.I_ampa_2[0] / nA)
  # plt.show()

  for spike_mon in spike_monitors:
    print(f'Number of {labels[spike_monitors.index(spike_mon)]} that fired: {len(set(spike_mon.i))}')
 
    plt.subplot(len(spike_monitors), 1, spike_monitors.index(spike_mon) + 1)
    plt.plot(spike_mon.t / ms, spike_mon.i, '|k', markersize=1)
    plt.xlabel('Time (ms)')
    plt.ylabel(f'{labels[spike_monitors.index(spike_mon)]} index')
  plt.show()


if __name__ == '__main__':
  main()

