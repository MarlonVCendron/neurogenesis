from brian2 import *
from utils.args_config import args

alpha_nmda = (args.nmda or 11) * ms  # NMDA scaling factor
alpha_ampa = (args.ampa or 5) * ms   # AMPA scaling factor
alpha_gaba = (args.gaba or 6) * ms   # GABA scaling factor

def synapse(receptor):
  R = receptor

  eq_model = Equations(f'''
    I_synapse  = g_syn * (Vm - E)                           : amp
    g_syn      = g_max * g                                  : siemens
    dg/dt      = -g / tau_r + (h * alpha) / (tau_r * tau_d) : 1 (clock-driven)
    dh/dt      = -h / tau_d                                 : 1 (clock-driven)

    I_{R}_post = I_synapse                                  : amp (summed)
  ''')

  eq_params = Equations('''
    g_max : siemens         # Synaptic strength
    E     : volt            # Reversal potential
    tau_r : second          # Rise time
    tau_d : second          # Decay time
    w     = 1     : 1       # Synaptic weight
  ''')

  on_pre = 'h += w'

  is_nmda  = R.startswith('nmda')
  is_ampa  = R.startswith('ampa')
  eq_alpha = Equations(f'alpha = {alpha_nmda if is_nmda else alpha_ampa if is_ampa else alpha_gaba} : second')

  eqs = eq_model + eq_params + eq_alpha

  return (eqs, on_pre)