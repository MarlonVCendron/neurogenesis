import nest

#  Params taken from doi.org/10.1007/s11571-024-10110-3

mc_params = {
    "E_L": -64.0,
    "g_L": 4.53,
    "C_m": 252.1,
    "V_reset": -49.0,
    "V_th": -42.0,
    "Delta_T": 2.0,
    "a": 1.0,
    "tau_w": 180.0,
    "b": 82.9,
    "E_rev": [],
    "tau_syn": [],
}

nest.CopyModel("aeif_cond_alpha_multisynapse", "mc", params=mc_params)
