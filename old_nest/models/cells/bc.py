import nest

#  Params taken from doi.org/10.1007/s11571-024-10110-3

bc_params = {
    "E_L": -52.0,
    "g_L": 18.054,
    "C_m": 17.93,
    "V_reset": -45.0,
    "V_th": -39.0,
    "Delta_T": 2.0,
    "a": 0.1,
    "tau_w": 100.0,
    "b": 20.5,
    "E_rev": [],
    "tau_syn": [],
}

nest.CopyModel("aeif_cond_alpha_multisynapse", "bc", params=bc_params)
