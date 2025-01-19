from brian2 import *
from neurogenesis.models.general.lif import LIF
from neurogenesis.models.cells import (gc, mc, bc, hipp)

start_scope()

print(gc)
run(100*ms)


# state_mon = StateMonitor(bc, 'Vm', record=True)
# spike_mon = SpikeMonitor(bc)

# run(100*ms)

# figure(figsize=(12, 4))
# subplot(121)
# plot(state_mon.t / ms, state_mon.Vm[0] / mV)
# xlabel('Time (ms)')
# ylabel('Membrane potential (mV)')
# subplot(122)
# plot(spike_mon.t / ms, spike_mon.i, '|k')
# xlabel('Time (ms)')
# ylabel('Neuron index')
# tight_layout
# show()
