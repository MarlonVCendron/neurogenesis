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
        "model"      : "izhikevich",
        "k"          : 0.45,
        "a"          : 0.003,
        "b"          : 24.48,
        "d"          : 50,
        "Cm"         : 38 * pF,
        "Vr"         : -77.4 * mV,
        "Vt"         : -44.9 * mV,
        "Vpeak"      : 15.49 * mV,
        "Vmin"       : -66.47 * mV,
    },
    "igc": { # TODO: Make it more excitable
        "name"       : "igc",
        "N"          : N_igc,
        "model"      : "izhikevich",
        "k"          : 0.45,
        "a"          : 0.003,
        "b"          : 24.48,
        "d"          : 50,
        "Cm"         : 38 * pF,
        "Vr"         : -77.4 * mV,
        "Vt"         : -44.9 * mV,
        "Vpeak"      : 15.49 * mV,
        "Vmin"       : -66.47 * mV,
    },
    "mc": {
        "name"      : "mc",
        "N"         : N_mc,
        "model"     : "izhikevich",
        "k"          : 1.5,
        "a"          : 0.004,
        "b"          : -20.84,
        "d"          : 117,
        "Cm"         : 258 * pF,
        "Vr"         : -63.67 * mV,
        "Vt"         : -37.11 * mV,
        "Vpeak"      : 28.29 * mV,
        "Vmin"       : -47.98 * mV,
    },
    "bc": {
        "name"       : "bc",
        "N"          : N_bc,
        "model"      : "izhikevich",
        "k"          : 0.81,
        "a"          : 0.097,
        "b"          : 1.89,
        "d"          : 553,
        "Cm"         : 208 * pF,
        "Vr"         : -61.02 * mV,
        "Vt"         : -37.84 * mV,
        "Vpeak"      : 14.08 * mV,
        "Vmin"       : -36.23 * mV,
    },
    "hipp": {
        "name"       : "hipp",
        "N"          : N_hipp,
        "model"      : "izhikevich",
        "k"          : 1.28,
        "a"          : 0.006,
        "b"          : 57.94,
        "d"          : -58,
        "Cm"         : 74 * pF,
        "Vr"         : -59.01 * mV,
        "Vt"         : -50.53 * mV,
        "Vpeak"      : 0.57 * mV,
        "Vmin"       : -56.98 * mV,
    },
    "pca3": {
        "name"      : "pca3",
        "N"         : N_pca3,
        "model"     : "izhikevich",
        "k"         : 0.79,
        "a"         : 0.008,
        "b"         : -42.55,
        "d"         : 588,
        "Cm"        : 366 * pF,
        "Vr"        : -63.2 * mV,
        "Vt"        : -33.6 * mV,
        "Vpeak"     : 35.86 * mV,
        "Vmin"      : -38.87 * mV,
    },
    # From Axo-axonic: https://hippocampome.org/php/neuron_page.php?id=2028
    "ica3": {
        "name"      : "ica3",
        "N"         : N_ica3,
        "model"     : "izhikevich",
        "k"         : 3.96,
        "a"         : 0.005,
        "b"         : 8.68,
        "d"         : 15,
        "Cm"        : 165 * pF,
        "Vr"        : -57.1 * mV,
        "Vt"        : -51.72 * mV,
        "Vpeak"     : 27.8 * mV,
        "Vmin"      : -73.97 * mV,
    },
}
