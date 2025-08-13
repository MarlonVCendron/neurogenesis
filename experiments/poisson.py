from brian2 import *
import numpy as np
import matplotlib.pyplot as plt

p = PoissonGroup(N=1, rates=40*Hz)

mon = SpikeMonitor(p)

net = Network(collect())
net.add(mon)

net.run(1000*ms)

plt.plot(mon.t / ms, mon.i, 'ok', markersize=4)
plt.axis('off')
plt.show()
