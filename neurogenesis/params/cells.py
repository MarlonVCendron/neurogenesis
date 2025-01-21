from brian2 import *

cell_params = {
    "bc": {
        "Cm"        : 232.6 * pF,
        "g_L"       : 23.2 * nS,
        "E_L"       : -62.0 * mV,
        "g_ahp_max" : 76.9 * nS,
        "tau_ahp"   : 2.0 * ms,
        "E_ahp"     : -75.0 * mV,
        "V_th"      : -52.5 * mV,
    },
    "hipp": {
        "Cm"        : 94.3 * pF,
        "g_L"       : 2.7 * nS,
        "E_L"       : -65.0 * mV,
        "g_ahp_max" : 52.0 * nS,
        "tau_ahp"   : 5.0 * ms,
        "E_ahp"     : -75.0 * mV,
        "V_th"      : -9.4 * mV,
    },
    "igc": {
        "Cm"        : 106.2 * pF,
        "g_L"       : 3.4 * nS,
        "E_L"       : -72.0 * mV,
        "g_ahp_max" : 10.4 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -53.4 * mV,
    },
    "mc": {
        "Cm"        : 206.0 * pF,
        "g_L"       : 5.0 * nS,
        "E_L"       : -62.0 * mV,
        "g_ahp_max" : 78.0 * nS,
        "tau_ahp"   : 10.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -32.0 * mV,
    },
    "mgc": {
        "Cm"        : 106.2 * pF,
        "g_L"       : 3.4 * nS,
        "E_L"       : -75.0 * mV,
        "g_ahp_max" : 10.4 * nS,
        "tau_ahp"   : 20.0 * ms,
        "E_ahp"     : -80.0 * mV,
        "V_th"      : -53.4 * mV,
    },
}
