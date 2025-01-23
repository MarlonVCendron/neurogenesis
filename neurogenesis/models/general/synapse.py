from brian2 import *

# These equations are all wrong
def synapse(receptor):
  R = receptor

  eq_model = Equations(f'''
    I_synapse  = g * (Vm - E)                  : amp
    g          = K * s                         : siemens
    s          = (y_d - y_r) / (tau_d - tau_r) : Hz
    dy_r/dt    = -y_r / tau_r                  : 1 (clock-driven)
    dy_d/dt    = -y_d / tau_d                  : 1 (clock-driven)
    I_{R}_post = I_synapse                     : amp (summed)
  ''')

  eq_params = Equations(f'''
    K     : siemens/hertz  # Synaptic strength
    E     : volt           # Reversal potential
    tau_r : second         # Rise time
    tau_d : second         # Decay time
    w     = 1 : 1          # Synaptic weight
  ''')

  on_pre = f'''
    y_r += w
    y_d += w
  '''

  eqs = eq_model + eq_params

  return (eqs, on_pre)
