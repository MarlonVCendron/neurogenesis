from brian2 import *

# These equations are all wrong
def synapse(receptor):
  R = receptor

  eq_model = Equations(f'''
    I_synapse    = g * (Vm - E)                  : amp
    g            = g_max * s                     : siemens
    ds/dt        = -s / tau_d + h0 * z * (1 - s) : 1 (clock-driven)
    dz/dt        = -z / tau_r                    : 1 (clock-driven)
    I_{R}_post   = I_synapse                     : amp (summed)
  ''')

  eq_params = Equations('''
    g_max : siemens             # Synaptic strength
    E     : volt                # Reversal potential
    tau_r : second              # Rise time
    tau_d : second              # Decay time
    w     = 1          : 1      # Synaptic weight
    h0    = 1 * ms**-1 : hertz  # TODO: this is a param
  ''')

  on_pre = 'z += w'

  eqs = eq_model + eq_params

  return (eqs, on_pre)
