from brian2 import *
import time
from neurogenesis.util import (lamellar_conn, cross_lamellar_conn)
from neurogenesis.models.synapses import (AMPA, NMDA, GABA)
from neurogenesis.models.cells import (
    create_gc,
    create_bc,
    create_mc,
    create_hipp,
)

N_lamellae = 20  # 20

N_gc_l   = 100
N_bc_l   = 1
N_mc_l   = 3
N_hipp_l = 1

N_gc   = N_lamellae * N_gc_l
N_bc   = N_lamellae * N_bc_l
N_mc   = N_lamellae * N_mc_l
N_hipp = N_lamellae * N_hipp_l

def main():
  start_time = time.time()
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

  # Lamellar connections
  gc_ampa_bc.connect(condition=lamellar_conn(N_gc_l, N_bc_l))
  gc_nmda_bc.connect(condition=lamellar_conn(N_gc_l, N_bc_l))
  gc_ampa_mc.connect(condition=lamellar_conn(N_gc_l, N_mc_l))
  gc_nmda_mc.connect(condition=lamellar_conn(N_gc_l, N_mc_l))
  gc_ampa_hipp.connect(condition=lamellar_conn(N_gc_l, N_hipp_l))
  gc_nmda_hipp.connect(condition=lamellar_conn(N_gc_l, N_hipp_l))
  
  bc_gaba_gc.connect(condition=lamellar_conn(N_bc_l, N_gc_l))
  bc_gaba_mc.connect(condition=lamellar_conn(N_bc_l, N_mc_l))
  
  mc_ampa_hipp.connect(condition=lamellar_conn(N_mc_l, N_hipp_l))
  mc_nmda_hipp.connect(condition=lamellar_conn(N_mc_l, N_hipp_l))
  
  hipp_gaba_gc.connect(condition=lamellar_conn(N_hipp_l, N_gc_l))
  hipp_gaba_bc.connect(condition=lamellar_conn(N_hipp_l, N_bc_l))
  hipp_gaba_mc.connect(condition=lamellar_conn(N_hipp_l, N_mc_l))

  # Cross-lamellar connections
  mc_ampa_gc.connect(condition=cross_lamellar_conn(N_mc_l, N_gc_l), p=0.2)
  mc_nmda_gc.connect(condition=cross_lamellar_conn(N_mc_l, N_gc_l), p=0.2)
  mc_ampa_bc.connect(condition=cross_lamellar_conn(N_mc_l, N_bc_l), p=0.2)
  mc_nmda_bc.connect(condition=cross_lamellar_conn(N_mc_l, N_bc_l), p=0.2)
  
  time_to_connect = time.time()
  print("--- Time to connect: %s seconds ---" % (time_to_connect - start_time))

  run(100*ms)

  print("--- Time to run simulation: %s seconds ---" % (time.time() - time_to_connect))


if __name__ == '__main__':
  main()

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
