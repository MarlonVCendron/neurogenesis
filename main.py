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

  print('Created cells')

  # Synapses
  ec_ampa_mgc = Connect(ec, mgc, **syn_params['ec_ampa_mgc'])
  ec_nmda_mgc = Connect(ec, mgc, **syn_params['ec_nmda_mgc'])
  ec_ampa_igc = Connect(ec, igc, **syn_params['ec_ampa_igc'])
  ec_nmda_igc = Connect(ec, igc, **syn_params['ec_nmda_igc'])

  mgc_ampa_bc   = Connect(mgc, bc, **syn_params['mgc_ampa_bc'])
  mgc_nmda_bc   = Connect(mgc, bc, **syn_params['mgc_nmda_bc'])
  mgc_ampa_mc   = Connect(mgc, mc, **syn_params['mgc_ampa_mc'])
  mgc_nmda_mc   = Connect(mgc, mc, **syn_params['mgc_nmda_mc'])
  mgc_ampa_hipp = Connect(mgc, hipp, **syn_params['mgc_ampa_hipp'])
  mgc_nmda_hipp = Connect(mgc, hipp, **syn_params['mgc_nmda_hipp'])

  igc_ampa_bc   = Connect(igc, bc, **syn_params['igc_ampa_bc'])
  igc_nmda_bc   = Connect(igc, bc, **syn_params['igc_nmda_bc'])
  igc_ampa_mc   = Connect(igc, mc, **syn_params['igc_ampa_mc'])
  igc_nmda_mc   = Connect(igc, mc, **syn_params['igc_nmda_mc'])
  igc_ampa_hipp = Connect(igc, hipp, **syn_params['igc_ampa_hipp'])
  igc_nmda_hipp = Connect(igc, hipp, **syn_params['igc_nmda_hipp'])

  bc_gaba_mgc = Connect(bc, mgc, **syn_params['bc_gaba_mgc'])
  bc_gaba_mc  = Connect(bc, mc, **syn_params['bc_gaba_mc'])

  mc_ampa_mgc  = Connect(mc, mgc, **syn_params['mc_ampa_mgc'])
  mc_nmda_mgc  = Connect(mc, mgc, **syn_params['mc_nmda_mgc'])
  mc_ampa_igc  = Connect(mc, igc, **syn_params['mc_ampa_igc'])
  mc_nmda_igc  = Connect(mc, igc, **syn_params['mc_nmda_igc'])
  mc_ampa_bc   = Connect(mc, bc, **syn_params['mc_ampa_bc'])
  mc_nmda_bc   = Connect(mc, bc, **syn_params['mc_nmda_bc'])
  mc_ampa_hipp = Connect(mc, hipp, **syn_params['mc_ampa_hipp'])
  mc_nmda_hipp = Connect(mc, hipp, **syn_params['mc_nmda_hipp'])

  hipp_gaba_mgc = Connect(hipp, mgc, **syn_params['hipp_gaba_mgc'])
  hipp_gaba_bc  = Connect(hipp, bc, **syn_params['hipp_gaba_bc'])
  hipp_gaba_mc  = Connect(hipp, mc, **syn_params['hipp_gaba_mc'])

  print('Created connections')

  neurons = [ec, mgc, igc, bc, mc, hipp]
  labels = [neuron.name for neuron in neurons]
  spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]

  net = Network(collect())
  net.add(spike_monitors)

  print('Running simulation')
  net.run(400*ms)
  
  for spike_mon in spike_monitors:
    print(f'Number of {labels[spike_monitors.index(spike_mon)]} that fired: {len(set(spike_mon.i))}')
 
    plt.subplot(len(spike_monitors), 1, spike_monitors.index(spike_mon) + 1)
    plt.plot(spike_mon.t / ms, spike_mon.i, '|k')
    plt.xlabel('Time (ms)')
    plt.ylabel(f'{labels[spike_monitors.index(spike_mon)]} index')
  plt.show()
  # plt.savefig('neurogenesis/figures/spikes.png')
  # plt.close()



if __name__ == '__main__':
  main()

