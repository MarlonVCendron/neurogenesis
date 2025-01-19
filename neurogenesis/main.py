from brian2 import *
from neurogenesis.models.synapses import (AMPA, NMDA, GABA)
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

  # Cells
  gc   = create_gc(N=N_gc)
  bc   = create_bc(N=N_bc)
  mc   = create_mc(N=N_mc)
  hipp = create_hipp(N=N_hipp)

  # Synapses
  ampa_eqs = AMPA()
  nmda_eqs = NMDA()
  gaba_eqs = GABA()

  gc_ampa_bc   = Synapses(gc, bc, model=ampa_eqs)
  gc_nmda_bc   = Synapses(gc, bc, model=nmda_eqs)
  gc_ampa_mc   = Synapses(gc, mc, model=ampa_eqs)
  gc_nmda_mc   = Synapses(gc, mc, model=nmda_eqs)
  gc_ampa_hipp = Synapses(gc, hipp, model=ampa_eqs)
  gc_nmda_hipp = Synapses(gc, hipp, model=nmda_eqs)

  bc_gaba_gc = Synapses(bc, gc, model=gaba_eqs)
  bc_gaba_mc = Synapses(bc, mc, model=gaba_eqs)

  mc_ampa_gc   = Synapses(mc, gc, model=ampa_eqs)
  mc_nmda_gc   = Synapses(mc, gc, model=nmda_eqs)
  mc_ampa_bc   = Synapses(mc, bc, model=ampa_eqs)
  mc_nmda_bc   = Synapses(mc, bc, model=nmda_eqs)
  mc_ampa_hipp = Synapses(mc, hipp, model=ampa_eqs)
  mc_nmda_hipp = Synapses(mc, hipp, model=nmda_eqs)

  hipp_gaba_gc = Synapses(hipp, gc, model=gaba_eqs)
  hipp_gaba_bc = Synapses(hipp, bc, model=gaba_eqs)
  hipp_gaba_mc = Synapses(hipp, mc, model=gaba_eqs)

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
