from brian2 import *
from utils.args_config import args

RECEPTOR_PARAMS = {
    'nmda': {'alpha': args.nmda or 10, 'E': 0 * mV},
    'ampa': {'alpha': args.ampa or 10, 'E': 0 * mV},
    'gaba': {'alpha': args.gaba or 10, 'E': -75 * mV}, # TODO: Check if this is correct
}

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
    tau_r : second           # Rise time
    tau_d : second           # Decay time
    w     = 1          : 1   # Synaptic weight
    beta  = 4 * ms**-1 : Hz  # Synaptic scaling factor
  ''')

  on_pre = 'h += w'

  receptor_prefix = R.split('_')[0]
  
  alpha_val = RECEPTOR_PARAMS[receptor_prefix]['alpha']
  E_val = RECEPTOR_PARAMS[receptor_prefix]['E']
  
  eq_alpha  = Equations(f'alpha = {alpha_val}*ms : second')
  eq_E      = Equations(f'E = {E_val / mV} * mV : volt')

  eqs = eq_model + eq_params + eq_alpha + eq_E

  return (eqs, on_pre)