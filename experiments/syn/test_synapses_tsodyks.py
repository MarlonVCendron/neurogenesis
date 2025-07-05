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
    create_hipp,
)

seed(1)

defaultclock.dt = 0.1 * ms

def to_100(params):
  return {**params, "p": 1.0, "condition": None}

# params = {
#     "syn_type" : "exc",
#     "syn_var"  : 1,
#     "p"        : 1,
#     "g"        : 1 * nS,
#     "tau_r"    : 750 * ms,
#     "tau_d"    : 20 * ms,
#     "tau_f"    : 50 * ms,
#     "U_se"     : 0.45,
#     "delay"    : 1.0 * ms
# }

# params = {
#     "syn_type" : "exc",
#     "syn_var"  : 1,
#     "p"        : 1,
#     "g"        : 1 * nS,
#     "tau_r"    : 50 * ms,
#     "tau_d"    : 20 * ms,
#     "tau_f"    : 750 * ms,
#     "U_se"     : 0.15,
#     "delay"    : 1.0 * ms
# }

def main():
  start_scope()

  # pp  = create_pp(N=1, active_p=1.0, rate=40*Hz, init_rates=True)

  indices = array([0, 0, 0, 0, 0])
  times = array([15, 90, 150, 200, 230])*ms
  # mgc = SpikeGeneratorGroup(1, indices, times)
  mgc = PoissonGroup(15, rates=20*Hz)

  mc      = create_mc(N=1)

  mgc_mc  = Connect(mgc, mc, **to_100(syn_params['mgc_mc']))

  mon = StateMonitor(mc, True, record=True)
  mon_s = SpikeMonitor(mc)
  mon_r = PopulationRateMonitor(mc)
  mon_syn = StateMonitor(mgc_mc, ['U', 'R', 'A'], record=True)

  net = Network(collect())

  # pp_mgc.g = 40 * nS

  print('Running simulation')
  net.run(500 * ms)

  # smooth_rates = mon_r.smooth_rate(window='flat', width=50*ms) / Hz

  # spike_count = mon_s.count
  # print(spike_count)
  # print(f'Mean rate: {np.mean(smooth_rates)}')

  # plot_voltage(mon, mon_s)
  plot_voltage(mon)

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




  plt.plot(mon_syn.t / ms, mon_syn.U[0])
  plt.plot(mon_syn.t / ms, mon_syn.R[0])
  plt.plot(mon_syn.t / ms, mon_syn.A[0])
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.D[0])
  # plt.plot(mon_syn_pp.t / ms, mon_syn_pp.R[0] + mon_syn_pp.A[0] + mon_syn_pp.D[0])
  plt.plot(mon.t / ms, mon.I_syn[0] / nA)
  plt.legend(['U', 'R', 'A', 'I_syn'])
  plt.xticks(rotation=45)
  plt.locator_params(axis="x", nbins=60)
  plt.grid(True, which="both", linestyle="--", alpha=0.2)
  plt.show()


if __name__ == '__main__':
  main()

