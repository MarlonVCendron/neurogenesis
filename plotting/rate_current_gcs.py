from brian2 import *
import matplotlib.pyplot as plt
import numpy as np
from plotting.voltage import plot_voltage
from models.cells import (create_mgc, create_igc)

start_scope()

mgc = create_mgc(N=1)
igc = create_igc(N=1)

# mgc_M = PopulationRateMonitor(mgc)
# igc_M = PopulationRateMonitor(igc)

mgc_M = SpikeMonitor(mgc)
igc_M = SpikeMonitor(igc)

mon = StateMonitor(mgc, True, record=True)

store()

sim_time = 3000 * ms
# sim_time = 50 * ms
rates = []

# r = np.arange(40, 120)
# ran = np.unique(np.round(r**1.1).astype(int))
# for i in np.arange(70, 120):
for i in np.arange(65, 200):
# for i in np.arange(80, 81):
# for i in np.arange(200, 201):
  restore()

  curr = i * pA
  mgc.I_ext = curr
  igc.I_ext = curr

  mgc_M.active = False
  igc_M.active = False
  run(100*ms)
  mgc_M.active = True
  igc_M.active = True
  run(sim_time)

  # plot_voltage(mon, mgc_M)

  # plt.plot(mon.t / ms, mon.g_ahp[0] / nS)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.ylabel('g_AHP (nS)')
  # plt.show()
  
  # plt.plot(mon.t / ms, mon.w_ahp[0])
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.ylabel('w_AHP')
  # plt.show()

  # plt.plot(mon.t / ms, mon.I_ahp[0] / nA)
  # plt.xticks(rotation=45)
  # plt.locator_params(axis="x", nbins=60)
  # plt.grid(True, which="both", linestyle="--", alpha=0.2)
  # plt.ylabel('I_AHP (nA)')
  # plt.show()

  # mgc_rate = mgc_M.rate[0]  # / Hz
  # igc_rate = igc_M.rate[0]  # / Hz
  mgc_rate = mgc_M.num_spikes / (sim_time)
  igc_rate = igc_M.num_spikes / (sim_time)
  rates.append((curr/pA, mgc_rate/Hz, igc_rate/Hz))
  print(f'Current: {curr}, MGC rate: {mgc_rate}, IGC rate: {igc_rate}')

# Plot frequency vs. current

fig, ax = plt.subplots()
ax.plot([curr for curr, _, _ in rates], [mgc_rate for _, mgc_rate, _ in rates], label='MGC')
ax.plot([curr for curr, _, _ in rates], [igc_rate for _, _, igc_rate in rates], label='IGC')
ax.set_xlabel('Current (pA)')
ax.set_ylabel('Frequency (Hz)')
ax.legend()
plt.savefig('figures/rate_current_gcs.png')
# plt.show()
plt.close()
