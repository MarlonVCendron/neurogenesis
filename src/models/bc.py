import nest

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
}

nest.CopyModel("aeif_cond_alpha", "bc", params=bc_params)
