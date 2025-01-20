from brian2 import *
import time
from neurogenesis.util import (lamellar_conn, cross_lamellar_conn)
from neurogenesis.models.synapses import (AMPA, NMDA, GABA)
from neurogenesis.models.cells import (
    create_mgc,
    create_bc,
    create_mc,
    create_hipp,
    create_ec,
)

N_lamellae = 20  # 20

N_mgc_l  = 100
N_bc_l   = 1
N_mc_l   = 3
N_hipp_l = 1

N_ec   = 400
N_mgc  = N_lamellae * N_mgc_l
N_bc   = N_lamellae * N_bc_l
N_mc   = N_lamellae * N_mc_l
N_hipp = N_lamellae * N_hipp_l

def main():
  start_time = time.time()
  start_scope()

  # Cells
  ec   = create_ec(N=N_ec)
  mgc  = create_mgc(N=N_mgc)
  bc   = create_bc(N=N_bc)
  mc   = create_mc(N=N_mc)
  hipp = create_hipp(N=N_hipp)

  # Synapses
  ec_mgc = Synapses(ec, mgc, 'w = 0.07 * pA : amp', on_pre='I_ampa -= w')
  ec_mgc.connecat(p=0.2)

  ampa_eqs = AMPA()
  nmda_eqs = NMDA()
  gaba_eqs = GABA()

  mgc_ampa_bc   = Synapses(mgc, bc, model=ampa_eqs)
  mgc_nmda_bc   = Synapses(mgc, bc, model=nmda_eqs)
  mgc_ampa_mc   = Synapses(mgc, mc, model=ampa_eqs)
  mgc_nmda_mc   = Synapses(mgc, mc, model=nmda_eqs)
  mgc_ampa_hipp = Synapses(mgc, hipp, model=ampa_eqs)
  mgc_nmda_hipp = Synapses(mgc, hipp, model=nmda_eqs)

  bc_gaba_mgc = Synapses(bc, mgc, model=gaba_eqs)
  bc_gaba_mc  = Synapses(bc, mc, model=gaba_eqs)

  mc_ampa_mgc  = Synapses(mc, mgc, model=ampa_eqs)
  mc_nmda_mgc  = Synapses(mc, mgc, model=nmda_eqs)
  mc_ampa_bc   = Synapses(mc, bc, model=ampa_eqs)
  mc_nmda_bc   = Synapses(mc, bc, model=nmda_eqs)
  mc_ampa_hipp = Synapses(mc, hipp, model=ampa_eqs)
  mc_nmda_hipp = Synapses(mc, hipp, model=nmda_eqs)

  hipp_gaba_mgc = Synapses(hipp, mgc, model=gaba_eqs)
  hipp_gaba_bc  = Synapses(hipp, bc, model=gaba_eqs)
  hipp_gaba_mc  = Synapses(hipp, mc, model=gaba_eqs)

  # Lamellar connections
  mgc_ampa_bc.connect(condition=lamellar_conn(N_mgc_l, N_bc_l))
  mgc_nmda_bc.connect(condition=lamellar_conn(N_mgc_l, N_bc_l))
  mgc_ampa_mc.connect(condition=lamellar_conn(N_mgc_l, N_mc_l))
  mgc_nmda_mc.connect(condition=lamellar_conn(N_mgc_l, N_mc_l))
  mgc_ampa_hipp.connect(condition=lamellar_conn(N_mgc_l, N_hipp_l))
  mgc_nmda_hipp.connect(condition=lamellar_conn(N_mgc_l, N_hipp_l))
  
  bc_gaba_mgc.connect(condition=lamellar_conn(N_bc_l, N_mgc_l))
  bc_gaba_mc.connect(condition=lamellar_conn(N_bc_l, N_mc_l))
  
  mc_ampa_hipp.connect(condition=lamellar_conn(N_mc_l, N_hipp_l))
  mc_nmda_hipp.connect(condition=lamellar_conn(N_mc_l, N_hipp_l))
  
  hipp_gaba_mgc.connect(condition=lamellar_conn(N_hipp_l, N_mgc_l))
  hipp_gaba_bc.connect(condition=lamellar_conn(N_hipp_l, N_bc_l))
  hipp_gaba_mc.connect(condition=lamellar_conn(N_hipp_l, N_mc_l))

  # Cross-lamellar connections
  mc_ampa_mgc.connect(condition=cross_lamellar_conn(N_mc_l, N_mgc_l), p=0.2)
  mc_nmda_mgc.connect(condition=cross_lamellar_conn(N_mc_l, N_mgc_l), p=0.2)
  mc_ampa_bc.connect(condition=cross_lamellar_conn(N_mc_l, N_bc_l), p=0.2)
  mc_nmda_bc.connect(condition=cross_lamellar_conn(N_mc_l, N_bc_l), p=0.2)
  
  time_to_connect = time.time()
  print("--- Time to connect: %s seconds ---" % (time_to_connect - start_time))

  run(100*ms)

  print("--- Time to run simulation: %s seconds ---" % (time.time() - time_to_connect))

  spike_mon = SpikeMonitor(mgc)
  
  run(400*ms)
  
  plot(spike_mon.t / ms, spike_mon.i, '|k')
  xlabel('Time (ms)')
  ylabel('Neuron index')
  tight_layout
  show()



if __name__ == '__main__':
  main()

