from brian2 import *
from neurogenesis.util import heaviside


def GABA():
  eq_model = Equations('''
    I_gaba_syn = g_gaba * (Vm - E_gaba) : amp
    g_gaba     = k_gaba * s_gaba        : siemens
    s_gaba     : 1
    # ds_gaba/dt = 1                      : 1
  ''')

  eq_params = Equations('''
    k_gaba     : siemens  # Synaptic strength
    E_gaba     : volt     # Reversal potential
    tau_gaba_l : second   # Latency time
    tau_gaba_r : second   # Rise time
    tau_gaba_d : second   # Decay time
  ''')

  eqs = eq_model + eq_params

  return eqs
