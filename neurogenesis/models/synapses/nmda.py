from brian2 import *
from neurogenesis.util import heaviside


def NMDA():
  eq_model = Equations('''
    I_nmda     = g_nmda * (Vm - E_nmda) : amp
    g_nmda     = k_nmda * s_nmda        : siemens
    ds_nmda/dt = 1                      : 1
  ''')

  eq_params = Equations('''
    k_nmda     : siemens  # Synaptic strength
    E_nmda     : volt     # Reversal potential
    tau_nmda_l : second   # Latency time
    tau_nmda_r : second   # Rise time
    tau_nmda_d : second   # Decay time
  ''')

  eqs = eq_model + eq_params

  return eqs
