from brian2 import *
from params.general import N_lamellae, has_igc
from utils.args_config import args

N_pp   = args.n_pp
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
        "name"       : "mgc",
        "N"          : N_mgc,
        "model"      : "adex",
        "Cm"         : 6.78 * pF,
        "g_L"        : 0.2639 * nS,
        "E_L"        : -87.0 * mV,
        "V_th"       : -56.0 * mV,
        "DeltaT"     : 0.0 * mV,
        "a"          : 2.0 * nS,
        "b"          : 0.045 * nA,
        "tau_o"      : 45.0 * ms,
        "V_reset"    : -74.0 * mV,
        "alpha_nmda" : 2 * ms**-1,
        "eta"        : 0.2 * mM**-1,
        "gamma"      : 0.04 * mV**-1,
        "Mg_conc"    : 2 * mM
    },
    "igc": {
        "name"      : "igc",
        "N"         : N_igc,
        "model"     : "expif",
        "Cm"        : 20.0 * pF,
        "g_L"       : 0.2159 * nS,
        "E_L"       : -78.0 * mV,
        "V_th"      : -35.9 * mV,
        "DeltaT"    : 2.0 * mV,
        # "a"         : 0.0 * nS,
        # "b"         : 0.06 * nA,
        # "tau_o"     : 101.5 * ms,
        "V_reset"   : -63.0 * mV,
        "eta"        : 0.2 * mM**-1,
        "gamma"      : 0.04 * mV**-1,
        "Mg_conc"    : 2 * mM
    },
    "mc": {
        "name"      : "mc",
        "N"         : N_mc,
        "model"     : "adex",
        "Cm"        : 252.1 * pF,
        "g_L"       : 4.53 * nS,
        "E_L"       : -64.0 * mV,
        "V_th"      : -42.0 * mV,
        "DeltaT"    : 2.0 * mV,
        "a"         : 1.0 * nS,
        "b"         : 0.0829 * nA,
        "tau_o"     : 180.0 * ms,
        "V_reset"   : -49.0 * mV
    },
    "bc": {
        "name"      : "bc",
        "N"         : N_bc,
        "model"     : "adex",
        "Cm"        : 179.3 * pF,
        "g_L"       : 18.054 * nS,
        "E_L"       : -52.0 * mV,
        "V_th"      : -39.0 * mV,
        "DeltaT"    : 2.0 * mV,
        "a"         : 0.1 * nS,
        "b"         : 0.0205 * nA,
        "tau_o"     : 100.0 * ms,
        "V_reset"   : -45.0 * mV
    },
    "hipp": {
        "name"      : "hipp",
        "N"         : N_hipp,
        "model"     : "adex",
        "Cm"        : 58.4 * pF,
        "g_L"       : 1.93 * nS,
        "E_L"       : -59.0 * mV,
        "V_th"      : -50.0 * mV,
        "DeltaT"    : 2.0 * mV,
        "a"         : 0.82 * nS,
        "b"         : 0.015 * nA,
        "tau_o"     : 93.0 * ms,
        "V_reset"   : -56.0 * mV
    },
    # CA3 - INNACURATE PARAMS - TODO: FIX: https://hippocampome.org/php/ephys.php
    "pca3": {
        "name"      : "pca3",
        "N"         : N_pca3,
        "model"     : "adex",
        "Cm"        : 100.0 * pF,
        "g_L"       : 0.2639 * nS,
        "E_L"       : -87.0 * mV,
        "V_th"      : -56.0 * mV,
        "DeltaT"    : 0.0 * mV,
        "a"         : 2.0 * nS,
        "b"         : 0.045 * nA,
        "tau_o"     : 45.0 * ms,
        "V_reset"   : -74.0 * mV
    },
    "ica3": {
        "name"      : "ica3",
        "N"         : N_ica3,
        "model"     : "adex",
        "Cm"        : 100.0 * pF,
        "g_L"       : 0.2639 * nS,
        "E_L"       : -87.0 * mV,
        "V_th"      : -56.0 * mV,
        "DeltaT"    : 0.0 * mV,
        "a"         : 2.0 * nS,
        "b"         : 0.045 * nA,
        "tau_o"     : 45.0 * ms,
        "V_reset"   : -74.0 * mV
    },
}
