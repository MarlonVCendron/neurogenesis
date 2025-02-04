from brian2 import *

def synapse(receptor):
  R = receptor

  eq_model = Equations(f'''
    I_synapse = g_syn * (Vm - E)                                       : amp
    g_syn     = g_max * f * g                                          : siemens
    dg/dt     = -g/tau_d + h * 1/ms                                    : 1 (clock-driven)
    dh/dt     = -h/tau_r                                               : 1 (clock-driven)
    t_peak    = (tau_d * tau_r / (tau_d - tau_r)) * log(tau_d / tau_r) : second
    f         = 1 / (-exp(-t_peak / tau_r) + exp(-t_peak / tau_d))     : 1

    I_{R}_post = I_synapse                                              : amp (summed)
  ''')

  eq_params = Equations('''
    g_max : siemens  # Synaptic strength
    E     : volt     # Reversal potential
    tau_r : second   # Rise time
    tau_d : second   # Decay time
    w = 1 : 1        # Synaptic weight
  ''')

  on_pre = 'h += w'

  eqs = eq_model + eq_params

  return (eqs, on_pre)