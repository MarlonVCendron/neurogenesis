from brian2 import *

def LIF():
  eq_model = Equations('''
    dVm/dt = (-I_L -I_ahp -I_syn) / Cm                      : volt
    I_L    = g_L * (Vm - E_L)                               : amp
    I_ahp  = g_ahp * (Vm - E_ahp)                           : amp
    g_ahp  = g_ahp_max * e ** (- (t - lastspike) / tau_ahp) : siemens
    # I_syn   = I_ampa + I_nmda + I_gaba                     : amp
    # I_ampa  = g_ampa * (Vm - E_ampa)                       : amp
    # I_nmda  = g_nmda * (Vm - E_nmda)                       : amp
    # I_gaba  = g_gaba * (Vm - E_gaba)                       : amp
  ''')

  eq_params = Equations('''
    Cm        : farad    # Membrane capacitance
    g_L       : siemens  # Leak conductance
    E_L       : volt     # Leak reversal potential
    g_ahp_max : siemens  # Maximum AHP conductance
    tau_ahp   : second   # AHP time constant
    E_ahp     : volt     # AHP reversal potential
    V_th      : volt     # Threshold potential
    I_syn     : amp
  ''')

  eqs = eq_model + eq_params

  return eqs
