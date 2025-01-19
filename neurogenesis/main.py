from brian2 import *
from neurogenesis.models.general.lif import LIF
from neurogenesis.models.cells import (
    create_gc,
    create_bc,
    create_mc,
    create_hipp,
)

N_lamellae = 2                 # 20
N_gc       = N_lamellae * 100
N_bc       = N_lamellae * 1
N_mc       = N_lamellae * 3
N_hipp     = N_lamellae * 1

if __name__ == '__main__':
  start_scope()

  gc   = create_gc(N=N_gc)
  bc   = create_bc(N=N_bc)
  mc   = create_mc(N=N_mc)
  hipp = create_hipp(N=N_hipp)

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
