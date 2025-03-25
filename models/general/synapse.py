from brian2 import *

def synapse(receptor):
  R = receptor

  eq_model = Equations(f'''
    I_synapse  = g_syn * (Vm - E)                          : amp
    g_syn      = g_max * g                                 : siemens
    dg/dt      = (h * alpha) / (tau_r * tau_d) - g / tau_r : 1 (clock-driven)
    dh/dt      = -h / tau_d                                : 1 (clock-driven)

    I_{R}_post = I_synapse                                 : amp (summed)
  ''')

  eq_params = Equations('''
    g_max : siemens         # Synaptic strength
    E     : volt            # Reversal potential
    tau_r : second          # Rise time
    tau_d : second          # Decay time
    w     = 1     : 1       # Synaptic weight
    alpha = 10*ms : second  # Scaling factor
  ''')

  on_pre = 'h += w'

  eqs = eq_model + eq_params

  return (eqs, on_pre)