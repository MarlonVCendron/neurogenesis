from brian2 import *

def AMPA():
  eq_model = Equations('''
    I_ampa_syn = g_ampa * (Vm - E_ampa) : amp
    g_ampa     = k_ampa * s_ampa        : siemens
    s_ampa     : 1
    # ds_ampa/dt = 1                      : 1
    # e_ampa = (exp(-t/tau_ampa_d) - exp(-t/tau_ampa_r)) / (tau_ampa_d - tau_ampa_r) : 1
  ''')

  eq_params = Equations('''
    k_ampa     : siemens  # Synaptic strength
    E_ampa     : volt     # Reversal potential
    tau_ampa_l : second   # Latency time
    tau_ampa_r : second   # Rise time
    tau_ampa_d : second   # Decay time
  ''')

  eqs = eq_model + eq_params

  return eqs
