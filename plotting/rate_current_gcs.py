from brian2 import *
import matplotlib.pyplot as plt
import numpy as np
from models.cells import (create_mgc, create_igc)

start_scope()

mgc = create_mgc(N=1)
igc = create_igc(N=1)

# mgc_M = PopulationRateMonitor(mgc)
# igc_M = PopulationRateMonitor(igc)

mgc_M = SpikeMonitor(mgc)
igc_M = SpikeMonitor(igc)

store()

sim_time = 5000 * ms
rates = []

# r = np.arange(40, 120)
# ran = np.unique(np.round(r**1.1).astype(int))
for i in np.arange(50, 200):
  restore()

  curr = i * pA
  mgc.I_ext = curr
  igc.I_ext = curr

  run(sim_time)

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
plt.show()
plt.savefig('figures/rate_current_gcs.png')
plt.close()
