from brian2 import *
from utils.connect import Connect
from params import syn_params 
from params.cells import cell_params
from models.cells import (
    create_mgc,
    create_igc,
    create_bc,
    create_mc,
    create_hipp,
    create_pp,
    create_pca3,
    create_ica3,
)


def network(ca3=False):
  net = Network()
  
  pp   = create_pp(N=cell_params['pp']['N'])
  mgc  = create_mgc()
  igc  = create_igc()
  bc   = create_bc()
  mc   = create_mc()
  hipp = create_hipp()
  if ca3:
    pca3 = create_pca3()
    ica3 = create_ica3()
    net.add(pca3, ica3)

  pp_ampa_mgc = Connect(pp, mgc, **syn_params['pp_ampa_mgc'])
  pp_nmda_mgc = Connect(pp, mgc, **syn_params['pp_nmda_mgc'])
  pp_ampa_igc = Connect(pp, igc, **syn_params['pp_ampa_igc'])
  pp_nmda_igc = Connect(pp, igc, **syn_params['pp_nmda_igc'])
  pp_ampa_hipp = Connect(pp, hipp, **syn_params['pp_ampa_hipp'])
  pp_nmda_hipp = Connect(pp, hipp, **syn_params['pp_nmda_hipp'])

  mgc_ampa_bc   = Connect(mgc, bc, **syn_params['mgc_ampa_bc'])
  mgc_nmda_bc   = Connect(mgc, bc, **syn_params['mgc_nmda_bc'])
  mgc_ampa_mc   = Connect(mgc, mc, **syn_params['mgc_ampa_mc'])
  mgc_nmda_mc   = Connect(mgc, mc, **syn_params['mgc_nmda_mc'])

  igc_ampa_bc   = Connect(igc, bc, **syn_params['igc_ampa_bc'])
  igc_nmda_bc   = Connect(igc, bc, **syn_params['igc_nmda_bc'])
  igc_ampa_mc   = Connect(igc, mc, **syn_params['igc_ampa_mc'])
  igc_nmda_mc   = Connect(igc, mc, **syn_params['igc_nmda_mc'])

  bc_gaba_mgc = Connect(bc, mgc, **syn_params['bc_gaba_mgc'])
  bc_gaba_mc  = Connect(bc, mc, **syn_params['bc_gaba_mc'])

  mc_ampa_mgc  = Connect(mc, mgc, **syn_params['mc_ampa_mgc'])
  mc_nmda_mgc  = Connect(mc, mgc, **syn_params['mc_nmda_mgc'])
  mc_ampa_igc  = Connect(mc, igc, **syn_params['mc_ampa_igc'])
  mc_nmda_igc  = Connect(mc, igc, **syn_params['mc_nmda_igc'])
  mc_ampa_bc   = Connect(mc, bc, **syn_params['mc_ampa_bc'])
  mc_nmda_bc   = Connect(mc, bc, **syn_params['mc_nmda_bc'])

  hipp_gaba_mgc = Connect(hipp, mgc, **syn_params['hipp_gaba_mgc'])

  if ca3:
    pca3 = create_pca3()
    ica3 = create_ica3()
    net.add(pca3, ica3)

  net.add(collect())

  return net