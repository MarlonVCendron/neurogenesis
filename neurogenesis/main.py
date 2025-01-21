from brian2 import *
from neurogenesis.utils.connections import (lamellar_conn, cross_lamellar_conn)
from neurogenesis.utils.connect import Connect
from neurogenesis.params import syn_params 
from neurogenesis.params.cells import cell_params
from neurogenesis.models.cells import (
    create_mgc,
    create_igc,
    create_bc,
    create_mc,
    create_hipp,
    create_ec,
)

def main():
  start_scope()

  # Cells
  ec   = create_ec(N=cell_params['ec']['N'])
  mgc  = create_mgc(N=cell_params['mgc']['N'])
  igc  = create_igc(N=cell_params['igc']['N'])
  bc   = create_bc(N=cell_params['bc']['N'])
  mc   = create_mc(N=cell_params['mc']['N'])
  hipp = create_hipp(N=cell_params['hipp']['N'])

  # Synapses
  ec_mgc = Synapses(ec, mgc, 'w = 0.07 * pA : amp', on_pre='I_ampa -= w')
  ec_mgc.connect(p=0.2)

  # mgc_ampa_mc = Connect(mgc, mc, 'ampa', condition=lamellar_conn(N_mgc_l, N_mc_l), delay=1.5*ms, K=9.58*pF, E=0*mV, tau_r=0.5*ms, tau_d=6.2*ms)
  mgc_ampa_mc = Connect(mgc, mc, 'ampa', condition=lamellar_conn(N_mgc_l, N_mc_l), **syn_params['gc_ampa_mc'])
  mc_ampa_mgc = Connect(mc, mgc, 'ampa', condition=cross_lamellar_conn(N_mc_l, N_mgc_l), delay=3*ms, K=0.07*pF, E=0*mV, tau_r=0.1*ms, tau_d=2.5*ms)



  # mgc_ampa_bc   = Synapses(mgc, bc, model=ampa_eqs)
  # mgc_nmda_bc   = Synapses(mgc, bc, model=nmda_eqs)
  # mgc_ampa_mc   = Synapses(mgc, mc, model=ampa_eqs)
  # mgc_nmda_mc   = Synapses(mgc, mc, model=nmda_eqs)
  # mgc_ampa_hipp = Synapses(mgc, hipp, model=ampa_eqs)
  # mgc_nmda_hipp = Synapses(mgc, hipp, model=nmda_eqs)

  # bc_gaba_mgc = Synapses(bc, mgc, model=gaba_eqs)
  # bc_gaba_mc  = Synapses(bc, mc, model=gaba_eqs)

  # mc_ampa_mgc  = Synapses(mc, mgc, model=ampa_eqs)
  # mc_nmda_mgc  = Synapses(mc, mgc, model=nmda_eqs)
  # mc_ampa_bc   = Synapses(mc, bc, model=ampa_eqs)
  # mc_nmda_bc   = Synapses(mc, bc, model=nmda_eqs)
  # mc_ampa_hipp = Synapses(mc, hipp, model=ampa_eqs)
  # mc_nmda_hipp = Synapses(mc, hipp, model=nmda_eqs)

  # hipp_gaba_mgc = Synapses(hipp, mgc, model=gaba_eqs)
  # hipp_gaba_bc  = Synapses(hipp, bc, model=gaba_eqs)
  # hipp_gaba_mc  = Synapses(hipp, mc, model=gaba_eqs)

  # # Lamellar connections
  # mgc_ampa_bc.connect(condition=lamellar_conn(N_mgc_l, N_bc_l))
  # mgc_nmda_bc.connect(condition=lamellar_conn(N_mgc_l, N_bc_l))
  # mgc_ampa_mc.connect(condition=lamellar_conn(N_mgc_l, N_mc_l))
  # mgc_nmda_mc.connect(condition=lamellar_conn(N_mgc_l, N_mc_l))
  # mgc_ampa_hipp.connect(condition=lamellar_conn(N_mgc_l, N_hipp_l))
  # mgc_nmda_hipp.connect(condition=lamellar_conn(N_mgc_l, N_hipp_l))
  
  # bc_gaba_mgc.connect(condition=lamellar_conn(N_bc_l, N_mgc_l))
  # bc_gaba_mc.connect(condition=lamellar_conn(N_bc_l, N_mc_l))
  
  # mc_ampa_hipp.connect(condition=lamellar_conn(N_mc_l, N_hipp_l))
  # mc_nmda_hipp.connect(condition=lamellar_conn(N_mc_l, N_hipp_l))
  
  # hipp_gaba_mgc.connect(condition=lamellar_conn(N_hipp_l, N_mgc_l))
  # hipp_gaba_bc.connect(condition=lamellar_conn(N_hipp_l, N_bc_l))
  # hipp_gaba_mc.connect(condition=lamellar_conn(N_hipp_l, N_mc_l))

  # # Cross-lamellar connections
  # mc_ampa_mgc.connect(condition=cross_lamellar_conn(N_mc_l, N_mgc_l), p=0.2)
  # mc_nmda_mgc.connect(condition=cross_lamellar_conn(N_mc_l, N_mgc_l), p=0.2)
  # mc_ampa_bc.connect(condition=cross_lamellar_conn(N_mc_l, N_bc_l), p=0.2)
  # mc_nmda_bc.connect(condition=cross_lamellar_conn(N_mc_l, N_bc_l), p=0.2)
  
  spike_mon = SpikeMonitor(mgc)
  

  run(400*ms)
  
  plot(spike_mon.t / ms, spike_mon.i, '|k')
  xlabel('Time (ms)')
  ylabel('Neuron index')
  tight_layout
  show()



if __name__ == '__main__':
  main()

