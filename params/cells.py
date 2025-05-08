from brian2 import *
from params.general import N_lamellae, has_igc
from utils.args_config import args

N_pp     = args.n_pp
N_igc  = args.n_igc
N_mgc  = (args.n_mgc - args.n_igc) if has_igc else args.n_mgc
N_bc   = args.n_bc
N_mc   = args.n_mc
N_hipp = args.n_hipp
N_pca3 = args.n_pca3
N_ica3 = args.n_ica3

N_igc_l  = N_igc // N_lamellae
N_mgc_l  = N_mgc // N_lamellae
N_bc_l   = N_bc // N_lamellae
N_pca3_l = N_pca3 // N_lamellae
N_ica3_l = N_ica3 // N_lamellae

cell_params = {
    "pp": {
        "name"      : "pp",
        "N"         : N_pp
    },
    # Dentate gyrus
    "mgc": {
        "name"      : "mgc",
        "N"         : N_mgc,
        "Cm"        : 106.2 * pF,
        "g_L"       : 3.4 * nS,
        "E_L"       : -75.0 * mV,
        "g_ahp_max" : 10.4 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -51.5 * mV,
    },
    "igc": {
        "name"      : "igc",
        "N"         : N_igc,
        "Cm"        : 106.2 * pF,
        "g_L"       : 3.4 * nS,
        "E_L"       : -72.0 * mV,
        "g_ahp_max" : 10.4 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -51.5 * mV,
    },
    "mc": {
        "name"      : "mc",
        "N"         : N_mc,
        "Cm"        : 206.0 * pF,
        "g_L"       : 5.0 * nS,
        "E_L"       : -62.0 * mV,
        "g_ahp_max" : 78.0 * nS,
        "tau_ahp"   : 10.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -32.0 * mV,
    },
    "bc": {
        "name"      : "bc",
        "N"         : N_bc,
        "Cm"        : 232.6 * pF,
        "g_L"       : 23.2 * nS,
        "E_L"       : -62.0 * mV,
        "g_ahp_max" : 76.9 * nS,
        "tau_ahp"   : 2.0 * ms,
        "E_ahp"     : -75.0 * mV,
        "V_th"      : -52.5 * mV,
    },
    "hipp": {
        "name"      : "hipp",
        "N"         : N_hipp,
        "Cm"        : 94.3 * pF,
        "g_L"       : 2.7 * nS,
        "E_L"       : -65.0 * mV,
        "g_ahp_max" : 52.0 * nS,
        "tau_ahp"   : 5.0 * ms,
        "E_ahp"     : -75.0 * mV,
        "V_th"      : -9.4 * mV,
    },
    # CA3 - INNACURATE PARAMS - TODO: FIX: https://hippocampome.org/php/ephys.php
    "pca3": {
        "name"      : "pca3",
        "N"         : N_pca3,
        "Cm"        : 100.0 * pF,
        "g_L"       : 5.0 * nS,
        "E_L"       : -60.5 * mV,
        "g_ahp_max" : 10.0 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -50.0 * mV,
    },
    "ica3": {
        "name"      : "ica3",
        "N"         : N_ica3,
        "Cm"        : 100.0 * pF,
        "g_L"       : 5.0 * nS,
        "E_L"       : -75.0 * mV,
        "g_ahp_max" : 10.0 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -50.0 * mV,
    },
}
