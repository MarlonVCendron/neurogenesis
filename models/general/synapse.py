from brian2 import *
from utils.args_config import args

alpha_nmda = args.nmda or 10  # NMDA scaling factor
alpha_ampa = args.ampa or 10  # AMPA scaling factor
alpha_gaba = args.gaba or 10  # GABA scaling factor

def synapse(receptor):
  R = receptor

  eq_model = Equations(f'''
    I_synapse = g_syn * (Vm - E)                : amp
    g_syn     = g_max * g                       : siemens
    dg/dt     = -g / tau_d + h * (1 - g) * beta : 1 (clock-driven)
    dh/dt     = -h / tau_r                      : 1 (clock-driven)

    # dg/dt      = -g / tau_r + (h * alpha) / (tau_r * tau_d) : 1 (clock-driven)
    # dh/dt      = -h / tau_d                                 : 1 (clock-driven)

    I_{R}_post = I_synapse                                  : amp (summed)
  ''')

  eq_params = Equations('''
    g_max : siemens          # Synaptic strength
    E     : volt             # Reversal potential
    tau_r : second           # Rise time
    tau_d : second           # Decay time
    w     = 1          : 1   # Synaptic weight
    beta  = 4 * ms**-1 : Hz  # Synaptic scaling factor
  ''')

  on_pre = 'h += w'

  is_nmda   = R.startswith('nmda')
  is_ampa   = R.startswith('ampa')
  alpha_val = alpha_nmda if is_nmda else alpha_ampa if is_ampa else alpha_gaba
  eq_alpha  = Equations(f'alpha = {alpha_val}*ms : second')

  eqs = eq_model + eq_params + eq_alpha

  return (eqs, on_pre)