import nest

gc_params = {
    "E_L": -87.0,
    "g_L": 0.2639,
    "C_m": 6.8,
    "V_reset": -74.0,
    "V_th": -56.0,
    "Delta_T": 2.0, # Talvez seja 0 (lim)
    "a": 2.0,
    "tau_w": 45.0,
    "b": 45.0,
}

# Modelo talvez seja: adaptive integrate-and-fire model, não o exponencial
nest.CopyModel("aeif_cond_alpha", "gc", params=gc_params)
