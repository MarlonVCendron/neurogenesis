from brian2 import *
from utils.connect import Connect
from params import syn_params 
from params.cells import cell_params
from plotting.voltage import plot_voltage
from models.cells import (
    create_mgc,
    create_igc,
    create_mgc,
    create_mc,
    create_mgc,
    create_pp,
)

seed(1)

defaultclock.dt = 0.1 * ms

def to_100(params):
  return {**params, "p": 1.0}

def main():
  start_scope()

  # pp  = create_pp(N=1, active_p=1.0, rate=40*Hz, init_rates=True)

  indices = array([0])
  times = array([5])*ms
  # pp = SpikeGeneratorGroup(1, indices, times)
  pp = PoissonGroup(8, rates=40*Hz)

  # indices = array([0])
  # times = array([25])*ms
  mc = SpikeGeneratorGroup(1, indices, times)
  # mc = PoissonGroup(100, rates=2000*Hz)

  mgc      = create_mgc(N=1)

  pp_mgc  = Connect(pp, mgc, **to_100(syn_params['pp_mgc']))
  mc_mgc  = Connect(mc, mgc, **to_100(syn_params['mc_mgc']))

  mon = StateMonitor(mgc, True, record=True)
  mon_s = SpikeMonitor(mgc)
  mon_r = PopulationRateMonitor(mgc)
  mon_syn_pp = StateMonitor(pp_mgc, ['x', 'y', 'z', 'v'], record=True)

  net = Network(collect())

  pp_mgc.g = 40 * nS

  print('Running simulation')
  net.run(1000 * ms)

  smooth_rates = mon_r.smooth_rate(window='flat', width=50*ms) / Hz

  spike_count = mon_s.count
  print(spike_count)
  print(f'Mean rate: {np.mean(smooth_rates)}')

  plot_voltage(mon, mon_s)

  # plt.plot(mon.t / ms, mon.I_syn_1[0] / nA, alpha=0.7)
  # plt.plot(mon.t / ms, mon.I_syn_2[0] / nA, alpha=0.7)
  # plt.plot(mon.t / ms, mon.I_syn_3[0] / nA, alpha=0.7)
  # plt.plot(mon.t / ms, mon.I_syn_4[0] / nA, alpha=0.7)
  # plt.plot(mon.t / ms, mon.I_syn_5[0] / nA, alpha=0.7)
  # plt.legend(['I_syn_1', 'I_syn_2', 'I_syn_3', 'I_syn_4', 'I_syn_5'])
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.show()




  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.x[0])
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.y[0])
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.z[0])
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.v[0])
  # plt.legend(['x', 'y', 'z', 'v'])
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.show()


if __name__ == '__main__':
  main()

