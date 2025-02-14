from brian2 import *
from utils.utils import is_NMDA

def synapse(receptor):
  R = receptor

  eq_model = Equations(f'''
    I_syn_base = g_syn * (Vm - E)                                       : amp
    g_syn      = g_max * f * g                                          : siemens
    dg/dt      = -g/tau_d + h * 1/ms                                    : 1 (clock-driven)
    dh/dt      = -h/tau_r                                               : 1 (clock-driven)
    t_peak     = (tau_d * tau_r / (tau_d - tau_r)) * log(tau_d / tau_r) : second
    f          = 1 / (-exp(-t_peak / tau_r) + exp(-t_peak / tau_d))     : 1

    I_{R}_post = I_synapse                                              : amp (summed)
  ''')

  eq_params = Equations('''
    g_max : siemens  # Synaptic strength
    E     : volt     # Reversal potential
    tau_r : second   # Rise time
    tau_d : second   # Decay time
    w = 1 : 1        # Synaptic weight
  ''')

  eq_nmda = Equations('''
    I_synapse     = I_syn_base / gate_blockage           : amp
    gate_blockage = 1 + eta * mg_conc * exp(-gamma * Vm) : 1

    eta     : mmolar ** -1  # Sensitivity of Mg unblock
    mg_conc : mmolar        # Outer magnesium concentration
    gamma   : volt ** -1    # Steepness of Mg unblock
  ''')
  
  eq_other = Equations('''
    I_synapse  = I_syn_base : amp
  ''')

  eq_current = eq_nmda if is_NMDA(R) else eq_other
  eqs = eq_model + eq_params + eq_current

  on_pre = 'h += w'

  return (eqs, on_pre)