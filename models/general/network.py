from brian2 import *
from utils.connect import Connect
from params import cell_params, syn_params as default_syn_params, has_ca3, has_igc
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


def network(syn_params_arg=None):
  syn_params = syn_params_arg if syn_params_arg else default_syn_params
  net = Network()
  
  pp   = create_pp(N=cell_params['pp']['N'])
  mgc  = create_mgc()
  igc  = create_igc() if has_igc else None
  bc   = create_bc()
  mc   = create_mc()
  hipp = create_hipp()
  if has_ca3:
    pca3 = create_pca3()
    ica3 = create_ica3()
    net.add(collect())

  pp_mgc = Connect(pp, mgc, **syn_params['pp_mgc'])
  pp_mc  = Connect(pp, mc, **syn_params['pp_mc'])
  pp_igc = Connect(pp, igc, **syn_params['pp_igc']) if has_igc else None
  pp_bc  = Connect(pp, bc, **syn_params['pp_bc'])
  if has_ca3:
    pp_pca3 = Connect(pp, pca3, **syn_params['pp_pca3'])
    pp_ica3 = Connect(pp, ica3, **syn_params['pp_ica3'])
    net.add(collect())

  mgc_mc   = Connect(mgc, mc, **syn_params['mgc_mc'])
  mgc_hipp = Connect(mgc, hipp, **syn_params['mgc_hipp'])
  mgc_bc   = Connect(mgc, bc, **syn_params['mgc_bc'])
  if has_ca3:
    mgc_pca3 = Connect(mgc, pca3, **syn_params['mgc_pca3'])
    mgc_ica3 = Connect(mgc, ica3, **syn_params['mgc_ica3'])
    net.add(collect())  

  if has_igc:
    igc_mc   = Connect(igc, mc, **syn_params['igc_mc'])
    igc_hipp = Connect(igc, hipp, **syn_params['igc_hipp'])
    igc_bc   = Connect(igc, bc, **syn_params['igc_bc'])
    net.add(collect())
    if has_ca3:
      igc_pca3 = Connect(igc, pca3, **syn_params['igc_pca3'])
      igc_ica3 = Connect(igc, ica3, **syn_params['igc_ica3'])
      net.add(collect())

  mc_mgc  = Connect(mc, mgc, **syn_params['mc_mgc'])
  mc_igc  = Connect(mc, igc, **syn_params['mc_igc']) if has_igc else None
  mc_hipp = Connect(mc, hipp, **syn_params['mc_hipp'])
  mc_bc   = Connect(mc, bc, **syn_params['mc_bc'])

  hipp_mgc = Connect(hipp, mgc, **syn_params['hipp_mgc'])
  hipp_bc  = Connect(hipp, bc, **syn_params['hipp_bc'])

  bc_mgc  = Connect(bc, mgc, **syn_params['bc_mgc'])
  bc_igc  = Connect(bc, igc, **syn_params['bc_igc']) if has_igc else None
  bc_hipp = Connect(bc, hipp, **syn_params['bc_hipp'])

  if has_ca3:
    pca3_pca3 = Connect(pca3, pca3, **syn_params['pca3_pca3'])
    pca3_mc   = Connect(pca3, mc, **syn_params['pca3_mc'])
    pca3_ica3 = Connect(pca3, ica3, **syn_params['pca3_ica3'])

    ica3_pca3 = Connect(ica3, pca3, **syn_params['ica3_pca3'])

    net.add(collect())

  net.add(collect())

  return net