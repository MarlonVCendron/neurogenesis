from brian2 import *
from plotting.spikes_and_rates import plot_spikes_and_rates
from utils.connect import Connect
from params import syn_params 
from plotting.voltage import plot_voltage
from plotting.connectivity_matrices import connectivity_matrices
from params.general import results_dir
from models.cells import (
    create_mgc,
    create_igc,
    create_mgc,
    create_mc,
    create_hipp,
    create_pp,
)

set_device('cpp_standalone', build_on_run=False)

seed(1)

defaultclock.dt = 0.1 * ms

def to_100(params):
  return {**params, "p": 1.0}

def main():
  start_scope()

  pp   = create_pp(N=400, active_p=0.1, rate=40*Hz, init_rates=True)
  mgc  = create_mgc(N=2000)
  hipp = create_hipp(N=40)

  # pp_ampa_mgc  = Connect(pp, mgc, **to_100(syn_params['pp_ampa_mgc']))
  # pp_nmda_mgc  = Connect(pp, mgc, **to_100(syn_params['pp_nmda_mgc']))
  pp_ampa_mgc  = Connect(pp, mgc, **(syn_params['pp_ampa_mgc']))
  pp_nmda_mgc  = Connect(pp, mgc, **(syn_params['pp_nmda_mgc']))
  pp_ampa_hipp = Connect(pp, hipp, **syn_params['pp_ampa_hipp'])
  pp_nmda_hipp = Connect(pp, hipp, **syn_params['pp_nmda_hipp'])

  hipp_gaba_mgc = Connect(hipp, mgc, **syn_params['hipp_gaba_mgc'])

  # mon = StateMonitor(mgc, True, record=True)
  # mon_s = SpikeMonitor(mgc)
  # mon_syn_pp = StateMonitor(pp_ampa_mgc, ['g', 'h', 'g_syn', 'g_norm'], record=True)
  # mon_syn_pp = StateMonitor(pp_ampa_mgc, ['g', 'h', 'g_syn', 'f', 't_peak'], record=True)
  # mon_syn_pp = StateMonitor(pp_nmda_mgc, ['g', 'h', 'g_syn'], record=True)

  neurons = [pp, mgc, hipp]
  labels = [neuron.name for neuron in neurons]
  spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]
  rate_monitors = [PopulationRateMonitor(neuron) for neuron in neurons]
  mon = StateMonitor(mgc, True, record=True)

  net = Network(collect())
  net.add(spike_monitors)
  net.add(rate_monitors)

  print('Running simulation')
  break_time = 300 * ms
  stim_time = 1000 * ms

  pp.active = False
  net.run(break_time, report='text')
  pp.active = True
  net.run(stim_time, report='text')
  device.build()

  # plt.plot(mon.t / ms, mon.I_nmda[0] / nA)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.xlim(break_time/ms, (break_time+100*ms) / ms)
  # plt.show()

  # plt.plot(mon.t / ms, mon.I_gaba[0] / nA)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.xlim(break_time/ms, (break_time+100*ms) / ms)
  # plt.show()

  # plt.plot(mon.t / ms, mon.I_syn[0] / nA)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.xlim(break_time/ms, (break_time+100*ms) / ms)
  # plt.show()

  # plot_voltage(mon, mon_s)

  plot_spikes_and_rates(spike_monitors, rate_monitors, save=False)
  # for spike_mon in spike_monitors:
  #   rate = (spike_mon.num_spikes / len(spike_mon.source)) / stim_time
  #   print(f"Firing rate of {labels[spike_monitors.index(spike_mon)]}: {rate}")
  #   print(f'Number of {labels[spike_monitors.index(spike_mon)]} that fired: {len(set(spike_mon.i))}')
 
  #   plt.subplot(len(spike_monitors), 1, spike_monitors.index(spike_mon) + 1)
  #   plt.plot(spike_mon.t / ms, spike_mon.i, '|k', markersize=1)
  #   plt.xlabel('Time (ms)')
  #   plt.ylabel(f'{labels[spike_monitors.index(spike_mon)]} index')
  #   plt.xlim(break_time/ms, (break_time+stim_time) / ms)
  # plt.show()
  # connectivity_matrices(net, plot=False, filename="wta_connectivity_matrices.h5")


if __name__ == '__main__':
  main()

