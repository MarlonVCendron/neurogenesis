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
  pp = SpikeGeneratorGroup(1, indices, times)

  indices = array([0])
  times = array([25])*ms
  mc = SpikeGeneratorGroup(1, indices, times)

  mgc      = create_mgc(N=1)

  pp_ampa_mgc  = Connect(pp, mgc, **to_100(syn_params['pp_ampa_mgc']))
  pp_nmda_mgc  = Connect(pp, mgc, **to_100(syn_params['pp_nmda_mgc']))
  mc_ampa_mgc  = Connect(mc, mgc, **to_100(syn_params['mc_ampa_mgc']))
  mc_nmda_mgc  = Connect(mc, mgc, **to_100(syn_params['mc_nmda_mgc']))

  mon = StateMonitor(mgc, True, record=True)
  mon_s = SpikeMonitor(mgc)
  mon_syn_pp = StateMonitor(pp_nmda_mgc, ['s', 'h', 'g_syn'], record=True)

  net = Network(collect())

  print('Running simulation')
  net.run(50 * ms)

  plot_voltage(mon, mon_s)

  plt.plot(mon.t / ms, mon.I_ampa_1[0] / nA, alpha=0.7)
  plt.plot(mon.t / ms, mon.I_nmda_1[0] / nA, alpha=0.7)
  plt.plot(mon.t / ms, mon.I_ampa_2[0] / nA, alpha=0.7)
  plt.plot(mon.t / ms, mon.I_nmda_2[0] / nA, alpha=0.7)
  plt.plot(mon.t / ms, mon.I_ampa[0] / nA, alpha=0.7)
  plt.plot(mon.t / ms, mon.I_nmda[0] / nA, alpha=0.7)
  plt.plot(mon.t / ms, mon.I_syn[0] / nA, alpha=0.7)
  plt.legend(['I_ampa_1', 'I_nmda_1', 'I_ampa_2', 'I_nmda_2', 'I_ampa', 'I_nmda', 'I_syn'])
  plt.xticks(rotation=45)
  plt.locator_params(axis="x", nbins=60)
  plt.grid(True, which="both", linestyle="--", alpha=0.2)
  plt.show()




  # plt.plot(mon.t / ms, mon.I_syn[0] / nA)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.show()



  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.g_syn[0] / nS)
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.s[0])
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.h[0])
  # plt.legend(['g_syn', 's', 'h'])
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.show()

if __name__ == '__main__':
  main()

