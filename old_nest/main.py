import matplotlib.pyplot as plt
import nest

import models.gc
import models.bc
import models.mc

gc = nest.Create("gc", 1)
mc = nest.Create("mc", 1)
noise_ex = nest.Create("poisson_generator")

multimeter = nest.Create("multimeter", params={"record_from": ["V_m"]})
spikerecorder = nest.Create("spike_recorder")

nest.SetStatus(noise_ex, {"rate": 6000.0})

nest.Connect(noise_ex, mc, syn_spec={"weight": 4})
nest.Connect(mc, gc, syn_spec={"weight": 2})
nest.Connect(multimeter, gc)
nest.Connect(gc, spikerecorder)

nest.Simulate(1000.0)


# Data
dmm = multimeter.get()
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]

events = spikerecorder.get("events")
senders = events["senders"]
spike_ts = events["times"]

# Plotting V_m with spikes

fig, ax1 = plt.subplots()

color = "tab:blue"
ax1.set_xlabel("Time (ms)")
ax1.set_ylabel("V_m", color=color)
ax1.plot(ts, Vms, color=color)
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
color = "tab:red"
ax2.set_ylabel("Spikes", color=color)
ax2.vlines(spike_ts, 0, 1, color=color)
ax2.tick_params(axis="y", labelcolor=color)

fig.tight_layout()
plt.show()
