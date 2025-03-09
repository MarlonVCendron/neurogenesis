from brian2 import *
from utils.connect import Connect
from params import syn_params 
from params.cells import cell_params
from plotting.voltage import plot_voltage
from models.cells import (
    create_mgc,
    create_igc,
    create_bc,
    create_mc,
    create_hipp,
    create_pp,
)

seed(1)

defaultclock.dt = 0.1 * ms

def to_100(params):
  return {**params, "p": 1.0}

def main():
  start_scope()

  pp  = create_pp(N=8, active_p=1.0, rate=40*Hz, init_rates=True)
  # mgc     = create_mgc(N=1)
  bc      = create_bc(N=1)

  pp_ampa_bc  = Connect(pp, bc, **to_100(syn_params['pp_ampa_bc']))
  pp_nmda_bc  = Connect(pp, bc, **to_100(syn_params['pp_nmda_bc']))

  # mgc_ampa_bc   = Connect(mgc, bc, **to_100(syn_params['mgc_ampa_bc']))
  # mgc_nmda_bc   = Connect(mgc, bc, **to_100(syn_params['mgc_nmda_bc']))

  print('Created connections')

  # mon = StateMonitor(bc, 'Vm', record=True)
  mon = StateMonitor(bc, True, record=True)
  mon_s = SpikeMonitor(bc)
  # mon_syn_pp = StateMonitor(pp_ampa_bc, 'g_syn', record=True)
  mon_syn_pp = StateMonitor(pp_nmda_bc, 'g_syn', record=True)

  # neurons = [pp, mgc, bc]
  neurons = [pp, bc]
  labels = [neuron.name for neuron in neurons]
  spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]

  net = Network(collect())
  net.add(spike_monitors)

  print('Running simulation')
  duration = 1000 * ms
  # silent = 100 * ms
  # net.run(silent)
  # bc.I_ext = 0.25 * nA
  # net.run(duration - 2*silent)
  # bc.I_ext = 0.0 * nA
  # net.run(silent)

  net.run(duration)

  # plt.plot(mon.t / ms, mon.Vm[0] / mV)
  # plt.show()

  plot_voltage(mon, mon_s)

  # plt.plot(mon.t / ms, mon.I_ampa[0] / nA)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.show()

  # plt.plot(mon.t / ms, mon.I_L[0] / nA)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.show()

  # plt.plot(mon.t / ms, mon.I_ahp[0] / nA)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.show()

  plt.plot(mon_syn_pp.t / ms, mon_syn_pp.g_syn[0] / nS)
  plt.xticks(rotation=45)
  plt.locator_params(axis="x", nbins=60)
  plt.grid(True, which="both", linestyle="--", alpha=0.2)
  plt.show()

  # plt.subplot(2, 1, 1)
  # plt.plot(mon.t / ms, -1*mon.I_ampa_1[0] / nA, alpha=0.5)
  # plt.plot(mon.t / ms, -1*mon.I_ampa_2[0] / nA, alpha=0.5)
  # plt.plot(mon.t / ms, -1*mon.I_ampa[0] / nA, alpha=0.5) 
  # plt.subplot(2, 1, 2)
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.g_syn[0])
  # plt.plot(mon_syn_mgc.t / ms, mon_syn_mgc.g_syn[0])
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.g_syn[1])
  # plt.plot(mon_syn_mgc.t / ms, mon_syn_mgc.g_syn[1])
  # # plt.plot(mon.t / ms, mon.I_ampa_2[0] / nA)
  # plt.show()

  for spike_mon in spike_monitors:
    print(f"Firing rate of {labels[spike_monitors.index(spike_mon)]}: {spike_mon.num_spikes / duration}")
    print(f'Number of {labels[spike_monitors.index(spike_mon)]} that fired: {len(set(spike_mon.i))}')
 
    plt.subplot(len(spike_monitors), 1, spike_monitors.index(spike_mon) + 1)
    plt.plot(spike_mon.t / ms, spike_mon.i, '|k', markersize=1)
    plt.xlabel('Time (ms)')
    plt.ylabel(f'{labels[spike_monitors.index(spike_mon)]} index')
  plt.show()


if __name__ == '__main__':
  main()

