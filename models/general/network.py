from brian2 import *
from utils.connect import Connect
from params import cell_params, syn_params, ca3
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


def network():
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
    net.add(collect())
    # net.add(pca3, ica3)

  pp_ampa_mgc = Connect(pp, mgc, **syn_params['pp_ampa_mgc'])
  pp_nmda_mgc = Connect(pp, mgc, **syn_params['pp_nmda_mgc'])
  pp_ampa_igc = Connect(pp, igc, **syn_params['pp_ampa_igc'])
  pp_nmda_igc = Connect(pp, igc, **syn_params['pp_nmda_igc'])
  pp_ampa_hipp = Connect(pp, hipp, **syn_params['pp_ampa_hipp'])
  pp_nmda_hipp = Connect(pp, hipp, **syn_params['pp_nmda_hipp'])
  if ca3:
    pp_ampa_pca3 = Connect(pp, pca3, **syn_params['pp_ampa_pca3'])
    pp_nmda_pca3 = Connect(pp, pca3, **syn_params['pp_nmda_pca3'])
    net.add(collect())

  mgc_ampa_bc   = Connect(mgc, bc, **syn_params['mgc_ampa_bc'])
  mgc_nmda_bc   = Connect(mgc, bc, **syn_params['mgc_nmda_bc'])
  mgc_ampa_mc   = Connect(mgc, mc, **syn_params['mgc_ampa_mc'])
  mgc_nmda_mc   = Connect(mgc, mc, **syn_params['mgc_nmda_mc'])
  if ca3:
    mgc_ampa_pca3 = Connect(mgc, pca3, **syn_params['mgc_ampa_pca3'])
    mgc_nmda_pca3 = Connect(mgc, pca3, **syn_params['mgc_nmda_pca3'])
    mgc_ampa_ica3 = Connect(mgc, ica3, **syn_params['mgc_ampa_ica3'])
    mgc_nmda_ica3 = Connect(mgc, ica3, **syn_params['mgc_nmda_ica3'])
    net.add(collect())

  igc_ampa_mc   = Connect(igc, mc, **syn_params['igc_ampa_mc'])
  igc_nmda_mc   = Connect(igc, mc, **syn_params['igc_nmda_mc'])
  igc_ampa_hipp   = Connect(igc, hipp, **syn_params['igc_ampa_hipp'])
  igc_nmda_hipp   = Connect(igc, hipp, **syn_params['igc_nmda_hipp'])
  if ca3:
    igc_ampa_pca3 = Connect(igc, pca3, **syn_params['igc_ampa_pca3'])
    igc_nmda_pca3 = Connect(igc, pca3, **syn_params['igc_nmda_pca3'])
    igc_ampa_ica3 = Connect(igc, ica3, **syn_params['igc_ampa_ica3'])
    igc_nmda_ica3 = Connect(igc, ica3, **syn_params['igc_nmda_ica3'])
    net.add(collect())

  bc_gaba_mgc = Connect(bc, mgc, **syn_params['bc_gaba_mgc'])

  mc_ampa_mgc  = Connect(mc, mgc, **syn_params['mc_ampa_mgc'])
  mc_nmda_mgc  = Connect(mc, mgc, **syn_params['mc_nmda_mgc'])
  mc_ampa_igc  = Connect(mc, igc, **syn_params['mc_ampa_igc'])
  mc_nmda_igc  = Connect(mc, igc, **syn_params['mc_nmda_igc'])
  mc_ampa_bc   = Connect(mc, bc, **syn_params['mc_ampa_bc'])
  mc_nmda_bc   = Connect(mc, bc, **syn_params['mc_nmda_bc'])

  hipp_gaba_mgc = Connect(hipp, mgc, **syn_params['hipp_gaba_mgc'])
  hipp_gaba_igc = Connect(hipp, igc, **syn_params['hipp_gaba_igc'])

  if ca3:
    pca3_ampa_pca3 = Connect(pca3, pca3, **syn_params['pca3_ampa_pca3'])
    pca3_nmda_pca3 = Connect(pca3, pca3, **syn_params['pca3_nmda_pca3'])
    pca3_ampa_ica3 = Connect(pca3, ica3, **syn_params['pca3_ampa_ica3'])
    pca3_nmda_ica3 = Connect(pca3, ica3, **syn_params['pca3_nmda_ica3'])
    pca3_ampa_mc   = Connect(pca3, mc, **syn_params['pca3_ampa_mc'])
    pca3_nmda_mc   = Connect(pca3, mc, **syn_params['pca3_nmda_mc'])

    ica3_gaba_pca3 = Connect(ica3, pca3, **syn_params['ica3_gaba_pca3'])

    net.add(collect())

  net.add(collect())

  return net