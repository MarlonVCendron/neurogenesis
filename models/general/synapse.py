from brian2 import *
from utils.args_config import args

RECEPTOR_PARAMS = {
    'nmda': {'alpha': args.nmda, 'E': 0 * mV},
    'ampa': {'alpha': args.ampa, 'E': 0 * mV},
    'gaba': {'alpha': args.gaba, 'E': -75 * mV}, # TODO: Check if this is correct
}

def synapse(receptor) : 
  R        = receptor         # e.g. 'ampa_1'
  receptor = R.split('_')[0]  # e.g. 'ampa'

  alpha_val = RECEPTOR_PARAMS[receptor]['alpha']
  E_val = RECEPTOR_PARAMS[receptor]['E']

  if receptor == 'nmda':
    eq_I_synapse = Equations('I_synapse = I_pre_sat * (1.0/(1 + exp(-gamma*Vm)*(1.0/3.57))) : amp')
  else:
    eq_I_synapse = Equations('I_synapse = I_pre_sat : amp')
  
  eq_model = Equations(f'''
    I_pre_sat  = g_syn * (Vm - E)                 : amp
    g_syn      = g_max * s                        : siemens 
    ds/dt      = -s / tau_d + h * alpha * (1 - s) : 1 (clock-driven)
    dh/dt      = -h / tau_r                       : 1 (clock-driven)

    I_{R}_post = I_synapse                        : amp (summed)
  ''')

  # TODO: Each cell type has different Mg related parameters
  eq_params = Equations(f'''
    g_max : siemens                            # Synaptic strength
    tau_r : second                             # Rise time
    tau_d : second                             # Decay time
    w     = 1                    : 1           # Synaptic weight
    gamma = 0.072 * mV**-1       : volt**-1    # Mg Concentration factor
    E     = {E_val / mV} * mV    : volt        # Reversal potential
    alpha = {alpha_val} * ms**-1 : second**-1  # Scaling factor
  ''')

  on_pre = 'h += w'

  eqs = eq_model + eq_params + eq_I_synapse

  return (eqs, on_pre)