from brian2 import *
from utils.connections import lamellar_conn, cross_lamellar_conn, no_self_conn
from params.general import igc_conn
from params.cells import N_mgc_l, N_igc_l, N_bc_l, N_pca3_l, N_ica3_l, N_mc_l, N_hipp_l

syn_params = {
    "pp_mgc": {
        "syn_type" : "exc",
        "syn_var"  : 1,
        "p"        : 0.08,
        "g"        : 1.8246 * nS,
        "tau_r"    : 266.2388 * ms,
        "tau_d"    : 5.3332 * ms,
        "tau_f"    : 18.7138 * ms,
        "U_se"     : 0.2697,
        "delay"    : 1.0 * ms
    },
    "pp_igc": {
        "syn_type" : "exc",
        "syn_var"  : 1,
        "p"        : 0.08 * igc_conn,
        "g"        : 1.8246 * nS,
        "tau_r"    : 266.2388 * ms,
        "tau_d"    : 5.3332 * ms,
        "tau_f"    : 18.7138 * ms,
        "U_se"     : 0.2697,
        "delay"    : 1.0 * ms
    },
    "pp_mc": { # From MEC LII Stellate to DG Mossy MOLDEN
        "syn_type" : "exc",
        "syn_var"  : 1,
        # "p"        : 0.0085,
        "p"        : 0.2, # Because 20% of mossy cells are MOLDEN
        "g"        : 1.4222 * nS,
        "tau_d"    : 4.6711 * ms,
        "tau_r"    : 319.8348 * ms,
        "tau_f"    : 57.7657 * ms,
        "U_se"     : 0.2041,
        "delay"    : 1.0 * ms
    },
    "pp_bc": {
        "syn_type" : "exc",
        "syn_var"  : 1,
        # "p"        : 0.0256,
        "p"        : 0.2,
        "g"        : 1.4058 * nS,
        "tau_r"    : 144.4152 * ms,
        "tau_d"    : 3.8495 * ms,
        "tau_f"    : 48.2001 * ms,
        "U_se"     : 0.2137,
        "delay"    : 1.0 * ms
    },
    "pp_pca3": {
        "syn_type" : "exc",
        "syn_var"  : 1,
        "p"        : 0.04,
        "g"        : 1.0650 * nS,
        "tau_r"    : 258.3176 * ms,
        "tau_d"    : 6.5496 * ms,
        "tau_f"    : 53.4780 * ms,
        "U_se"     : 0.1840,
        "delay"    : 1.0 * ms
    },
    "pp_ica3": {
        "syn_type" : "exc",
        "syn_var"  : 1,
        "p"        : 0.2,
        "g"        : 1.5561 * nS,
        "tau_r"    : 457.4676 * ms,
        "tau_d"    : 3.6021 * ms,
        "tau_f"    : 35.9037 * ms,
        "U_se"     : 0.2096,
        "delay"    : 1.0 * ms
    },

    "mgc_mc": {
        "syn_type" : "exc",
        "syn_var"  : 2,
        # "p"        : 0.0078,
        "p"        : 0.2,
        "condition": lamellar_conn(N_mgc_l, N_mc_l),
        "g"        : 1.7130 * nS,
        "tau_r"    : 428.5826 * ms,
        "tau_d"    : 5.3469 * ms,
        "tau_f"    : 73.4791 * ms,
        "U_se"     : 0.1513,
        "delay"    : 1.0 * ms
    },
    "mgc_hipp": {
        "syn_type" : "exc",
        "syn_var"  : 1,
        # "p"        : 0.0059,
        "p"        : 0.1,
        "g"        : 1.3047 * nS,
        "tau_r"    : 462.8138 * ms,
        "tau_d"    : 5.1814 * ms,
        "tau_f"    : 48.9863 * ms,
        "U_se"     : 0.1503,
        "delay"    : 1.0 * ms
    },
    "mgc_bc": {
        "syn_type" : "exc",
        "syn_var"  : 2,
        # "p"        : 0.0035,
        "p"        : 1.0,
        "condition": lamellar_conn(N_mgc_l, N_bc_l),
        "g"        : 1.4575 * nS,
        "tau_r"    : 151.2653 * ms,
        "tau_d"    : 3.5662 * ms,
        "tau_f"    : 62.2781 * ms,
        "U_se"     : 0.1969,
        "delay"    : 1.0 * ms
    },
    "mgc_pca3": {
        "syn_type" : "exc",
        "syn_var"  : 2,
        "p"        : 0.6,
        "condition": lamellar_conn(N_mgc_l, N_pca3_l),
        "g"        : 1.3842 * nS,
        "tau_r"    : 278.2858 * ms,
        "tau_d"    : 6.6572 * ms,
        "tau_f"    : 78.5837 * ms,
        "U_se"     : 0.1553,
        "delay"    : 1.0 * ms
    },
    "mgc_ica3": {
        "syn_type" : "exc",
        "syn_var"  : 2,
        "p"        : 1.0,
        "condition": lamellar_conn(N_mgc_l, N_ica3_l),
        "g"        : 1.6245 * nS,
        "tau_r"    : 518.9344 * ms,
        "tau_d"    : 3.9147 * ms,
        "tau_f"    : 43.2742 * ms,
        "U_se"     : 0.1756,
        "delay"    : 1.0 * ms
    },

    "igc_mc": {
        "syn_type" : "exc",
        "syn_var"  : 3,
        "p"        : 0.2,
        "condition": lamellar_conn(N_igc_l, N_mc_l),
        "g"        : 1.7130 * nS,
        "tau_r"    : 428.5826 * ms,
        "tau_d"    : 5.3469 * ms,
        "tau_f"    : 73.4791 * ms,
        "U_se"     : 0.1513,
        "delay"    : 1.0 * ms
    },
    "igc_hipp": {
        "syn_type" : "exc",
        "syn_var"  : 2,
        "p"        : 0.1,
        "g"        : 1.3047 * nS,
        "tau_r"    : 462.8138 * ms,
        "tau_d"    : 5.1814 * ms,
        "tau_f"    : 48.9863 * ms,
        "U_se"     : 0.1503,
        "delay"    : 1.0 * ms
    },
    "igc_bc": {
        "syn_type" : "exc",
        "syn_var"  : 3,
        "p"        : 1.0,
        "condition": lamellar_conn(N_igc_l, N_bc_l),
        "g"        : 1.4575 * nS,
        "tau_r"    : 151.2653 * ms,
        "tau_d"    : 3.5662 * ms,
        "tau_f"    : 62.2781 * ms,
        "U_se"     : 0.1969,
        "delay"    : 1.0 * ms
    },
    "igc_pca3": {
        "syn_type" : "exc",
        "syn_var"  : 3,
        "p"        : 0.6,
        "condition": lamellar_conn(N_igc_l, N_pca3_l),
        "g"        : 1.3842 * nS,
        "tau_r"    : 278.2858 * ms,
        "tau_d"    : 6.6572 * ms,
        "tau_f"    : 78.5837 * ms,
        "U_se"     : 0.1553,
        "delay"    : 1.0 * ms
    },
    "igc_ica3": {
        "syn_type" : "exc",
        "syn_var"  : 3,
        "p"        : 1.0,
        "condition": lamellar_conn(N_igc_l, N_ica3_l),
        "g"        : 1.6245 * nS,
        "tau_r"    : 518.9344 * ms,
        "tau_d"    : 3.9147 * ms,
        "tau_f"    : 43.2742 * ms,
        "U_se"     : 0.1756,
        "delay"    : 1.0 * ms
    },

    "mc_mgc": {
        "syn_type" : "exc",
        "syn_var"  : 2,
        "p"        : 0.002,
        "condition": cross_lamellar_conn(N_mc_l, N_mgc_l),
        "g"        : 2.3943 * nS,
        "tau_r"    : 166.1625 * ms,
        "tau_d"    : 5.3570 * ms,
        "tau_f"    : 20.2241 * ms,
        "U_se"     : 0.3045,
        "delay"    : 1.0 * ms
    },
    "mc_igc": {
        "syn_type" : "exc",
        "syn_var"  : 2,
        "p"        : 0.002,
        "condition": cross_lamellar_conn(N_mc_l, N_igc_l),
        "g"        : 2.3943 * nS,
        "tau_r"    : 166.1625 * ms,
        "tau_d"    : 5.3570 * ms,
        "tau_f"    : 20.2241 * ms,
        "U_se"     : 0.3045,
        "delay"    : 1.0 * ms
    },
    # "mc_mc": {
    #     "syn_type" : "exc",
    #     "syn_var"  : 4,
    #     # "p"        : 0.0122,
    #     "p"        : 0.1,
    #     "condition": cross_lamellar_conn(N_mc_l, N_mc_l),
    #     "g"        : 2.0675 * nS,
    #     "tau_r"    : 249.3294 * ms,
    #     "tau_d"    : 4.2571 * ms,
    #     "tau_f"    : 71.6418 * ms,
    #     "U_se"     : 0.2446,
    #     "delay"    : 1.0 * ms
    # },
    "mc_hipp": {
        "syn_type" : "exc",
        "syn_var"  : 3,
        # "p"        : 0.0099,
        "p"        : 1.0,
        "condition": cross_lamellar_conn(N_mc_l, N_hipp_l),
        "g"        : 1.3762 * nS,
        "tau_r"    : 358.4310 * ms,
        "tau_d"    : 4.8235 * ms,
        "tau_f"    : 54.8716 * ms,
        "U_se"     : 0.1807,
        "delay"    : 1.0 * ms
    },
    "mc_bc": {
        "syn_type" : "exc",
        "syn_var"  : 4,
        # "p"        : 0.0117,
        "p"        : 1.0,
        "condition": cross_lamellar_conn(N_mc_l, N_bc_l),
        "g"        : 1.9956 * nS,
        "tau_r"    : 117.3654 * ms,
        "tau_d"    : 3.3955 * ms,
        "tau_f"    : 69.3164 * ms,
        "U_se"     : 0.2545,
        "delay"    : 1.0 * ms
    },

    "hipp_mgc": {
        "syn_type" : "inh",
        "syn_var"  : 3,
        # "p"        : 0.0060,
        "p"        : 0.2,
        "g"        : 2.0020 * nS,
        "tau_r"    : 559.1428 * ms,
        "tau_d"    : 8.9349 * ms,
        "tau_f"    : 8.3959 * ms,
        "U_se"     : 0.2781,
        "delay"    : 1.0 * ms
    },
    "hipp_bc": {
        "syn_type" : "inh",
        "syn_var"  : 5,
        # "p"        : 0.0061,
        "p"        : 0.02,
        "g"        : 1.7092 * nS,
        "tau_r"    : 367.1976 * ms,
        "tau_d"    : 5.9816 * ms,
        "tau_f"    : 15.2920 * ms,
        "U_se"     : 0.2209,
        "delay"    : 1.0 * ms
    },

    "bc_mgc": {
        "syn_type" : "inh",
        "syn_var"  : 4,
        # "p"        : 0.0064,
        "p"        : 1.0,
        "condition": lamellar_conn(N_bc_l, N_mgc_l),
        "g"        : 2.4509 * nS,
        "tau_r"    : 433.8758 * ms,
        "tau_d"    : 6.5435 * ms,
        "tau_f"    : 6.3474 * ms,
        "U_se"     : 0.3320,
        "delay"    : 1.0 * ms
    },
    "bc_igc": {
        "syn_type" : "inh",
        "syn_var"  : 3,
        "p"        : 1.0,
        "condition": lamellar_conn(N_bc_l, N_igc_l),
        "g"        : 2.4509 * nS,
        "tau_r"    : 433.8758 * ms,
        "tau_d"    : 6.5435 * ms,
        "tau_f"    : 6.3474 * ms,
        "U_se"     : 0.3320,
        "delay"    : 1.0 * ms
    },
    "bc_hipp": {
        "syn_type" : "inh",
        "syn_var"  : 4,
        # "p"        : 0.0044,
        "p"        : 0.02,
        "g"        : 1.4078 * nS,
        "tau_r"    : 534.1822 * ms,
        "tau_d"    : 6.5442 * ms,
        "tau_f"    : 8.3848 * ms,
        "U_se"     : 0.2405,
        "delay"    : 1.0 * ms
    },
    # "bc_bc": {
    #     "syn_type" : "inh",
    #     "syn_var"  : 6,
    #     # "p"        : 0.0044,
    #     "p"        : 0.2,
    #     "g"        : 1.9814 * nS,
    #     "tau_r"    : 195.5361 * ms,
    #     "tau_d"    : 4.6481 * ms,
    #     "tau_f"    : 7.4405 * ms,
    #     "U_se"     : 0.3095,
    #     "delay"    : 1.0 * ms
    # },

    "pca3_pca3": {
        "syn_type" : "exc",
        "syn_var"  : 4,
        "p"        : 0.02,
        "w"        : 0.1,
        "condition": no_self_conn(),
        "g"        : 0.6030 * nS,
        "tau_r"    : 278.2583 * ms,
        "tau_d"    : 9.5159 * ms,
        "tau_f"    : 27.5130 * ms,
        "U_se"     : 0.1724,
        "delay"    : 1.0 * ms
    },
    "pca3_mc": {
        "syn_type" : "exc",
        "syn_var"  : 5,
        "p"        : 0.1,
        "condition": lamellar_conn(N_pca3_l, N_mc_l),
        "g"        : 2.0355 * nS,
        "tau_d"    : 4.2967 * ms,
        "tau_r"    : 359.1159 * ms,
        "tau_f"    : 40.4567 * ms,
        "U_se"     : 0.2361,
        "delay"    : 1.0 * ms
    },
    "pca3_ica3": {
        "syn_type" : "exc",
        "syn_var"  : 4,
        "p"        : 1.0,
        "g"        : 1.2474 * nS,
        "tau_r"    : 525.6045 * ms,
        "tau_d"    : 4.5253 * ms,
        "tau_f"    : 23.3210 * ms,
        "U_se"     : 0.1890,
        "delay"    : 1.0 * ms
    },

    "ica3_pca3": {
        "syn_type" : "inh",
        "syn_var"  : 5,
        "p"        : 1.0,
        "g"        : 1.4622 * nS,
        "tau_r"    : 416.2817 * ms,
        "tau_d"    : 7.7927 * ms,
        "tau_f"    : 20.6297 * ms,
        "U_se"     : 0.2029,
        "delay"    : 1.0 * ms
    }
}