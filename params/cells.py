from brian2 import *
from params.general import N_lamellae, has_igc
from utils.args_config import args

scale = 1

N_pp   = args.n_pp * scale
N_igc  = (args.n_igc if has_igc else 0) * scale
N_mgc  = ((args.n_mgc - args.n_igc) if has_igc else args.n_mgc) * scale
N_bc   = args.n_bc * scale
N_mc   = args.n_mc * scale
N_hipp = args.n_hipp * scale
N_pca3 = args.n_pca3 * scale
N_ica3 = args.n_ica3 * scale

N_igc_l  = N_igc // N_lamellae
N_mgc_l  = N_mgc // N_lamellae
N_mc_l   = N_mc // N_lamellae
N_bc_l   = N_bc // N_lamellae
N_hipp_l = N_hipp // N_lamellae
N_pca3_l = N_pca3 // N_lamellae
N_ica3_l = N_ica3 // N_lamellae

cell_params = {
    "pp": {
        "name" : "pp",
        "N"    : N_pp
    },
    "mgc": {
        "name"  : "mgc",
        "N"     : N_mgc,
        "model" : "izhikevich",
        "k"     : 0.45 * nS / mV,
        "a"     : 0.003 * ms**-1,
        "b"     : 24.48 * nS,
        "d"     : 50 * pA,
        "Cm"    : 38 * pF,
        "Vr"    : -77.4 * mV,
        "Vt"    : -44.9 * mV,
        "Vpeak" : 15.49 * mV,
        "Vmin"  : -66.47 * mV,
    },
    "igc": { # Fit from "Neuronal Differentiation in the Adult Hippocampus Recapitulates Embryonic Development"
        "name"  : "igc",
        "N"     : N_igc,
        "model" : "izhikevich",
        "k"     : 0.1385 * nS / mV,
        "a"     : 0.0019 * ms**-1,
        "b"     : -1.8772 * nS,
        "d"     : 12.1494 * pA,
        "Cm"    : 24.6 * pF,
        "Vr"    : -63.66 * mV,
        "Vt"    : -38.41 * mV,
        "Vpeak" : 83.5 * mV,
        "Vmin"  : -48.2 * mV,
    },
    "mc": {
        "name"  : "mc",
        "N"     : N_mc,
        "model" : "izhikevich",
        "k"     : 1.5 * nS / mV,
        "a"     : 0.004 * ms**-1,
        "b"     : -20.84 * nS,
        "d"     : 117 * pA,
        "Cm"    : 258 * pF,
        "Vr"    : -63.67 * mV,
        "Vt"    : -37.11 * mV,
        "Vpeak" : 28.29 * mV,
        "Vmin"  : -47.98 * mV,
    },
    "bc": {
        "name"  : "bc",
        "N"     : N_bc,
        "model" : "izhikevich",
        "k"     : 0.81 * nS / mV,
        "a"     : 0.097 * ms**-1,
        "b"     : 1.89 * nS,
        "d"     : 553 * pA,
        "Cm"    : 208 * pF,
        "Vr"    : -61.02 * mV,
        "Vt"    : -37.84 * mV,
        "Vpeak" : 14.08 * mV,
        "Vmin"  : -36.23 * mV,
    },
    "hipp": { # From Izhikevich Models For Hippocampal Neurons And Its Sub-Region CA3
        "name"  : "hipp",
        "N"     : N_hipp,
        "model" : "izhikevich",
        "k"     : 0.01 * nS / mV,
        "a"     : 0.004 * ms**-1,
        "b"     : -2 * nS,
        "d"     : 40.52 * pA,
        "Cm"    : 58.7 * pF,
        "Vr"    : -70 * mV,
        "Vt"    : -50 * mV,
        "Vpeak" : 90 * mV,
        "Vmin"  : -75 * mV,
    },
    "pca3": {
        "name"  : "pca3",
        "N"     : N_pca3,
        "model" : "izhikevich",
        "k"     : 0.79 * nS / mV,
        "a"     : 0.008 * ms**-1,
        "b"     : -42.55 * nS,
        "d"     : 588 * pA,
        "Cm"    : 366 * pF,
        "Vr"    : -63.2 * mV,
        "Vt"    : -33.6 * mV,
        "Vpeak" : 35.86 * mV,
        "Vmin"  : -38.87 * mV,
    },
    # From Basket: https://hippocampome.org/php/neuron_page.php?id=2043
    "ica3": {
        "name"  : "ica3",
        "N"     : N_ica3,
        "model" : "izhikevich",
        "k"     : 1 * nS / mV,
        "a"     : 0.004 * ms**-1,
        "b"     : 9.26 * nS,
        "d"     : -6 * pA,
        "Cm"    : 45 * pF,
        "Vr"    : -57.51 * mV,
        "Vt"    : -23.38 * mV,
        "Vpeak" : 18.45 * mV,
        "Vmin"  : -47.56 * mV,
    },
}
