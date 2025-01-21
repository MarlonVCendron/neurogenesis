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
  mgc  = create_mgc()
  igc  = create_igc()
  bc   = create_bc()
  mc   = create_mc()
  hipp = create_hipp()

  # Synapses
  ec_mgc = Synapses(ec, mgc, 'w = 0.07 * pA : amp', on_pre='I_ampa -= w')
  ec_mgc.connect(p=0.2)

  mgc_ampa_bc   = Connect(mgc, bc, **syn_params['mgc_ampa_bc'])
  mgc_nmda_bc   = Connect(mgc, bc, **syn_params['mgc_nmda_bc'])
  mgc_ampa_mc   = Connect(mgc, mc, **syn_params['mgc_ampa_mc'])
  mgc_nmda_mc   = Connect(mgc, mc, **syn_params['mgc_nmda_mc'])
  mgc_ampa_hipp = Connect(mgc, hipp, **syn_params['mgc_ampa_hipp'])
  mgc_nmda_hipp = Connect(mgc, hipp, **syn_params['mgc_nmda_hipp'])

  bc_gaba_mgc = Connect(bc, mgc, **syn_params['bc_gaba_mgc'])
  bc_gaba_mc  = Connect(bc, mc, **syn_params['bc_gaba_mc'])

  mc_ampa_mgc  = Connect(mc, mgc, **syn_params['mc_ampa_mgc'])
  mc_nmda_mgc  = Connect(mc, mgc, **syn_params['mc_nmda_mgc'])
  mc_ampa_bc   = Connect(mc, bc, **syn_params['mc_ampa_bc'])
  mc_nmda_bc   = Connect(mc, bc, **syn_params['mc_nmda_bc'])
  mc_ampa_hipp = Connect(mc, hipp, **syn_params['mc_ampa_hipp'])
  mc_nmda_hipp = Connect(mc, hipp, **syn_params['mc_nmda_hipp'])

  hipp_gaba_mgc = Connect(hipp, mgc, **syn_params['hipp_gaba_mgc'])
  hipp_gaba_bc  = Connect(hipp, bc, **syn_params['hipp_gaba_bc'])
  hipp_gaba_mc  = Connect(hipp, mc, **syn_params['hipp_gaba_mc'])

  spike_mon = SpikeMonitor(mgc)

  run(400*ms)
  
  plot(spike_mon.t / ms, spike_mon.i, '|k')
  xlabel('Time (ms)')
  ylabel('Neuron index')
  tight_layout
  show()



if __name__ == '__main__':
  main()

