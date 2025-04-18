from brian2 import *
from params.general import N_lamellae, has_igc
from utils.args_config import args

N_pp     = args.n_pp
N_igc_l  = args.n_igc
N_mgc_l  = (args.n_mgc - N_igc_l) if has_igc else args.n_mgc
N_bc_l   = args.n_bc
N_mc_l   = args.n_mc
N_hipp_l = args.n_hipp
N_pca3_l = args.n_pca3
N_ica3_l = args.n_ica3

cell_params = {
    "pp": {
        "name"      : "pp",
        "N"         : N_pp
    },
    # Dentate gyrus
    "bc": {
        "name"      : "bc",
        "N"         : N_lamellae * N_bc_l,
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
        "N"         : N_lamellae * N_hipp_l,
        "Cm"        : 94.3 * pF,
        "g_L"       : 2.7 * nS,
        "E_L"       : -65.0 * mV,
        "g_ahp_max" : 52.0 * nS,
        "tau_ahp"   : 5.0 * ms,
        "E_ahp"     : -75.0 * mV,
        "V_th"      : -9.4 * mV,
    },
    "igc": {
        "name"      : "igc",
        "N"         : N_lamellae * N_igc_l,
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
        "N"         : N_lamellae * N_mc_l,
        "Cm"        : 206.0 * pF,
        "g_L"       : 5.0 * nS,
        "E_L"       : -62.0 * mV,
        "g_ahp_max" : 78.0 * nS,
        "tau_ahp"   : 10.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -32.0 * mV,
    },
    "mgc": {
        "name"      : "mgc",
        "N"         : N_lamellae * N_mgc_l,
        "Cm"        : 106.2 * pF,
        "g_L"       : 3.4 * nS,
        "E_L"       : -75.0 * mV,
        "g_ahp_max" : 10.4 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -51.5 * mV,
    },
    # CA3 - INNACURATE PARAMS
    "pca3": {
        "name"      : "pca3",
        "N"         : N_lamellae * N_pca3_l,
        "Cm"        : 100.0 * pF,
        "g_L"       : 5.0 * nS,
        "E_L"       : -75.0 * mV,
        "g_ahp_max" : 10.0 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -50.0 * mV,
    },
    "ica3": {
        "name"      : "ica3",
        "N"         : N_lamellae * N_ica3_l,
        "Cm"        : 100.0 * pF,
        "g_L"       : 5.0 * nS,
        "E_L"       : -75.0 * mV,
        "g_ahp_max" : 10.0 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -50.0 * mV,
    },
}
